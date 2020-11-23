import pandas as pd

class Member:
    def __init__(self, name, times, isSiteLeader, isStaff, canDrive, speakSpanish):
        self.name = name #String
        self.times = times #Boolean list with each index representing a different site
        self.isSiteLeader = isSiteLeader #Boolean
        self.isStaff = isStaff #Boolean
        self.canDrive = canDrive #Boolean
        self.speakSpanish = speakSpanish #Boolean
        self.assigned = False #Boolean
    
    def __eq__(self, other):
        return self.name == other.name
        
    def change_time(index):
        times[index] = not times[index]
    
    def assign(self):
        self.assigned = True
        
    def __str__(self):
        return self.name
    
class Site:
    def __init__(self, index, name, isDriving, requiresSpanish, maxNum):
        self.index = index #Index in times list corresponding to this site
        self.name = name #Name of site
        self.members = [] #List of members assigned to this site
        self.isDriving = isDriving #Boolean
        self.requiresSpanish = requiresSpanish #Boolean
        self.hasSiteLeader = False #Boolean
        self.maxNum = maxNum #Max number of site members

    def checkTime(self, member):
        return member.times[self.index]

    def add(self, member):
        self.members.append(member)
        member.assign()

    def delete(self, member):
        self.members.remove(member)
        member.assigned = False
    
    def size(self):
        return len(self.members)
    
    def __str__(self):
        ret = ""
        ret += "Site name: " + self.name + "\n"
        ret += "Site index: " + str(self.index) + "\n"
        ret += "Site driving: " + str(self.isDriving) + "\n"
        ret += "Site spanish speaking: " + str(self.requiresSpanish) + "\n"
        ret += "Site max num: " + str(self.maxNum) + "\n"
        ret += "Members: "
        for member in self.members:
            ret += member.name + ", "
        ret += "\n"
        return ret

#Creates list of all siteLeaders
def createSiteLeaderList(members):
    siteLeaders = []
    for member in members:
        if member.isSiteLeader:
            siteLeaders.append(member)
    return siteLeaders

#Creates list of all drivers
def createDriversList(members):
    drivers = []
    for member in members:
        if member.canDrive:
            drivers.append(member)
    return drivers

#Creates list of all spanish speakers
def createSpanishList(members):
    spanishSpeakers = []
    for member in members:
        if member.speakSpanish:
            spanishSpeakers.append(member)
    return spanishSpeakers


def assignSiteLeaders(members, sites):
    if len(members) == 0: return True
    member = members.pop(0)
    if member.assigned == True:
        return assignSiteLeaders(members, sites)
    else:
        for site in sites:
            if site.checkTime(member) and not site.hasSiteLeader:
                site.add(member)
                site.hasSiteLeader = True
                result = assignSiteLeaders(members, sites)
                if result: return result
                site.delete(member)
                site.hasSiteLeader = False
                members.append(member)
    return False

def assignDrivers(members, sites, driveSiteNum):
    if len(members) == 0 or driveSiteNum == 0: return True
    member = members.pop(0)
    if member.assigned == True:
        return assignDrivers(members, sites, driveSiteNum)
    else:
        for site in sites:
            if site.checkTime(member) and site.isDriving:
                site.add(member)
                site.isDriving = False
                result = assignDrivers(members, sites, driveSiteNum - 1)
                if result: return result
                site.delete(member)
                site.isDriving = True
                members.append(member)
    return False
        
def assignSpanish(members, site, spanishSiteNum):
    if len(members) == 0 or spanishSiteNum == 0: return True
    member = members.pop(0)
    if member.assigned == True:
        return assignSpanish(members, site, spanishSiteNum)
    else:
        for site in sites:
            if site.checkTime(member) and site.requiresSpanish:
                site.add(member)
                site.requiresSpanish = False
                result = assignSpanish(members, sites, spanishSiteNum - 1)
                if result: return result
                site.delete(member)
                site.requiresSpanish = True
                members.append(member)
    return False

def sort(drivers, spanish, siteLeaders, members, sites, driveSiteNum, spanishSiteNum):
    return assignSiteLeaders(siteLeaders, sites) and assignDrivers(drivers, sites, driveSiteNum) and assignSpanish(spanish, sites, spanishSiteNum) and recursiveSort(members, sites)
    
def recursiveSort(members, sites):
    if len(members) == 0: return True
    member = members.pop(0)
    if member.assigned == True:
        return recursiveSort(members, sites)
    else:
        for site in sites:
            if site.checkTime(member) and len(site.members) < site.maxNum:
                site.add(member)
                result = recursiveSort(members, sites)
                if result: return result
                site.delete(member)
                members.append(member)
    return False

membersExcel = pd.read_excel("~/Downloads/TempForm(Responses).xlsx") #File path to the excel file of member data
sitesExcel = pd.read_excel("~/Downloads/Sites.xlsx") #File path to the excel file of site to index mappings
staffExcel = pd.read_excel("~/Downloads/Site_Leaders.xlsx") #File path to the excel file of staff and site leaders

#process members
staffMembers = staffExcel["Staff Members"].tolist()
siteLeaders = staffExcel[staffExcel["Site Leaders"].notnull().tolist()]["Site Leaders"].tolist()

print(siteLeaders)

members = []
#Iterate through all members
for ind in membersExcel.index:
    #Iterate through all member info
    if pd.isnull(membersExcel["Timestamp"][ind]):
        continue
    times = []
    name = ""
    drive = False
    spanish = False
    staff = False
    site = False
    for col in membersExcel.columns:
        if col == "Name":
            name = membersExcel[col][ind]
        if col == "Drive":
            drive = True if membersExcel[col][ind] == "Yes" else False
        if col == "Spanish":
            spanish = True if membersExcel[col][ind] == "Yes" else False
        if "Availabilities" in col:
            times.append(True if membersExcel[col][ind] == "Yes" else False)
        if name in staffMembers:
            staff = True
        if name in siteLeaders:
            site = True
    newMember = Member(name, times, site, staff, drive, spanish)
    members.append(newMember)

drivers = createDriversList(members)
siteLeaders = createSiteLeaderList(members)
spanishSpeakers = createSpanishList(members)

#process sites
driveSiteNum = 0
spanishSiteNum = 0
maxNum = len(members) // len(siteExcel.index) + 1 #maximum members per site
index = 0
sites = []

for ind in siteExcel.index:
    name = ""
    drive = False
    spanish = False
    for col in siteExcel.columns:
        if col == "Name":
            name = siteExcel[col][ind]
        if col == "Driving":
            drive = True if siteExcel[col][ind] == "Yes" else False
            driveSiteNum = driveSiteNum + 1 if drive else driveSiteNum
        if col == "Spanish":
            spanish = True if siteExcel[col][ind] == "Yes" else False
            spanishSiteNum = spanishSiteNum + 1 if spanish else spanishSiteNum
    newSite = Site(index, name, drive, spanish, maxNum)
    sites.append(newSite)
    index += 1
    
complete = sort(drivers, spanishSpeakers, siteLeaders, members, sites, driveSiteNum, spanishSiteNum)
if complete:
    print("sorting complete")
else:
    print("sorting incomplete")
for site in sites:
    print(site)