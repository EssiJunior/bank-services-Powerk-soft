from pydantic import BaseSettings


class Settings(BaseSettings):
    # database_hostname: str 
    # database_port: str 
    # database_password: str 
    # database_name: str 
    # database_username: str 
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    super_admin_key: str
    


settings = Settings(secret_key="0e2hhj353333j3l4jlad2hjahdljfk3jl3j4lj34lj3l4eaaadadadjl34j",
                    algorithm="HS256",
                    access_token_expire_minutes=2880,
                    super_admin_key="Powerk-soft"
                    )
