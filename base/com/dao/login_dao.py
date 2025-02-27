from base import db
from base.com.vo.login_vo import LoginVO
from base.utils.my_logger import get_logger

logger = get_logger()


class LoginDao:
    def insert_login(self, login_vo):
        try:
            # Store the password as it is (in plain text)
            db.session.add(login_vo)
            db.session.commit()
            logger.info(f"Inserted login with ID: {login_vo.login_id}")
            return login_vo.login_id
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inserting login: {str(e)}")
            raise

    def validate_login(self, username, password):
        try:
            # Retrieve user by username
            user = LoginVO.query.filter_by(login_username=username).first()
            print("User found:", user)
            logger.info(f"Query Result for username {username}: {user}")

            if user:
                # hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user.login_password == password:
                    logger.info(f"User {username} validated successfully.")
                    print("User validated successfully.")
                    return user
                else:
                    logger.warning(f"Invalid password for user: {username}")
            else:
                logger.warning(f"User not found: {username}")

            return None
        except Exception as e:
            logger.error(f"Error validating login: {str(e)}")
            raise
