from collections import defaultdict

class Profile:
    def __init__(self, user ,password):
        self.user = user
        self.password = password
        self.accounts = defaultdict(dict)
        self.drive = None
    
    def get_drive(self):
        return self.drive
    
    def set_drive(self, drive):
        self.drive = drive

    def get_user(self)->str:
        return self.user

    def get_password(self)->str:
        return self.password

    def set_user(self,user):
        self.user = user

    def set_password(self,password):
        self.password = password

    def add_site(self, site,username, accountPassword):
        if site in self.accounts:
            if username in self.accounts[site]:
                return False
        self.accounts[str(site)][str(username)]=str(accountPassword)
        return True

    def update_password(self, site, username, newPassword):
        if site in self.accounts:
            if username in self.accounts[str(site)]:
                self.accounts[str(site)][str(username)]=str(newPassword)
            else:
                print("There is currently no account associated with " + site + " with credentials: " + username)
        else:
            print("You do not currently have an account associated with the site: " + site)

    def list_sites(self):
        sites = []
        for a in self.accounts:
            sites.append(a)
        return sites

    def get_accounts(self):
        return self.accounts

    def get_usernames(self):
        usernames = set()
        for a in self.accounts:
            for b in self.accounts[str(a)]:
                usernames.add(b)
        return usernames

    def search_user(self, username):
        result = defaultdict(dict)
        for a in self.accounts:
            if username in self.accounts[a]:
                result[a][username]=self.accounts[a][username]
        return result

    def delete_user(self, site, username):
        if site in self.accounts:
            if username in self.accounts[site]:
                del self.accounts[site][username]
                if len(self.accounts[site]) == 0:
                    del self.accounts[site]
                return True
            else:
                print("randerror")
                return False
        else:
            print("You do not currently have an account associated with the site: " + site)
            return False

    def delete_site(self, site):
        if site in self.accounts:
            del self.accounts[site]
        else:
            print("You do not currently have an account associated with the site: " + site)