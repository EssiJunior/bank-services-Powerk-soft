from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed(password: str):
    return password_context.hash(password)


def verified(password: str, db_password: str):
    return password_context.verify(password, db_password)


#-----------------------------/ Useful messages /-----------------------------#
SuperAdminException = ["Incorrect super admin key (Contact: +237 690743737)", "Sorry, super admin functionality."]
AdminException = ["Sorry, admin functionality."]
BankException = ["The specified acronym does not identify a bank in our system. "]
UserException = ["Not a user.", "Sorry, user functionality.", "Sorry,Users should belong to the same bank.", "Cannot transfer to yourself, (see Deposit)"]
EntryException = ["Incorrect password", "Entries 'password' et 'confirm_password' are different"]
no_account = "You don't have an account"
