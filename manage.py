import argparse
import sys

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.configs import settings
from app.helpers.password_hash import hash_password
from app.models.user_model import Users


def build_engine():
    return create_engine(f"postgresql://{settings.DATABASE_URL}")


def get_session() -> Session:
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=build_engine())
    return session_local()


def create_user(username: str, email: str, password: str, is_active: bool) -> int:
    normalized_email = email.strip().lower()
    hashed_password = hash_password(password)

    session = get_session()
    try:
        exists_stmt = select(Users.id).where(func.lower(Users.email) == normalized_email)
        existing_user_id = session.execute(exists_stmt).scalar_one_or_none()
        if existing_user_id is not None:
            print(f"User already exists with email: {normalized_email}")
            return 1

        user = Users(
            username=username.strip(),
            email=normalized_email,
            hashed_password=hashed_password,
            is_active=is_active,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        print("User created successfully")
        print(f"- id: {user.id}")
        print(f"- username: {user.username}")
        print(f"- email: {user.email}")
        print(f"- is_active: {user.is_active}")
        return 0
    except Exception as error:
        session.rollback()
        print(f"Create user failed: {error}")
        return 1
    finally:
        session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project management commands")
    subparsers = parser.add_subparsers(dest="command")

    create_user_parser = subparsers.add_parser("create-user", help="Create a new user")
    create_user_parser.add_argument("--username", required=True, help="Username")
    create_user_parser.add_argument("--email", required=True, help="Email")
    create_user_parser.add_argument("--password", required=True, help="Plain password")
    create_user_parser.add_argument(
        "--inactive",
        action="store_true",
        help="Create user with is_active=false (default is true)",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create-user":
        return create_user(
            username=args.username,
            email=args.email,
            password=args.password,
            is_active=not args.inactive,
        )

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
