from collections import defaultdict

class Profile:
    def __init__(self, user ,password):
        self.user = user
        self.password = password
        self.accounts = defaultdict(dict)

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def addSite(self, site,username, accountPassword):
        if site in self.accounts:
            if username in self.accounts[site]:
                return False
        self.accounts[str(site)][str(username)]=str(accountPassword)
        return True

    def updatePassword(self, site, username, newPassword):
        if site in self.accounts:
            if username in self.accounts[str(site)]:
                self.accounts[str(site)][str(username)]=str(newPassword)
            else:
                print("There is currently no account associated with " + site + " with credentials: " + username)
        else:
            print("You do not currently have an account associated with the site: " + site)

    def listSites(self):
        sites = []
        for a in self.accounts:
            sites.append(a)
        return sites

    def getAccounts(self):
        return self.accounts

    def listAll(self):
        for a in self.accounts:
            print(a)
            for b in self.accounts[str(a)]:
                print(b, ' : ', self.accounts[a][b])
    
    def searchSite(self, site):
        if site in self.accounts:
            print("Here are the accounts registered with " + site)
            for a in self.accounts[str(site)]:
                print(a, ':', self.accounts[site][a])
        else:
            print("You do not currently have an account associated with the site: " + site)

    def searchUser(self, username):
        result = defaultdict(dict)
        for a in self.accounts:
            if username in self.accounts[a]:
                result[a][username]=self.accounts[a][username]
        """
        if len(result) == 0:
            print("There are no accounts under " + username + " stored in this program")
            return
        else:
            print("Here are the list of accounts under " + username + " grouped by their associated site and passwords")
            for site in self.accounts:
                print(site)
                for user in result[str(site)]:
                    print(user, ' : ', self.accounts[site][user])
        """
        return result

    def deleteUser(self, site, username):
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

    def deleteSite(self, site):
        if site in self.accounts:
            del self.accounts[site]
        else:
            print("You do not currently have an account associated with the site: " + site)