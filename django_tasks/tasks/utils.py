import bcrypt


class BCryptPasswordUtil:

    UTF_8 = "utf-8"

    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode(BCryptPasswordUtil.UTF_8), bcrypt.gensalt()
        ).decode(BCryptPasswordUtil.UTF_8)

    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(BCryptPasswordUtil.UTF_8),
            hashed_password.encode(BCryptPasswordUtil.UTF_8),
        )
