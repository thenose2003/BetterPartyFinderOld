class handler():
    def __init__(self, version):
        self.version = version

    def result(self, skill, averageSkill, work, totalWork, **kwargs):
        return skill + ((averageSkill/skill)*(((work*100)/totalWork)-20))

    def newSkill(self, profile, work, totalWork, **kwargs):
        return self.result(profile[1], profile[1], work, totalWork)

    def findProfile(self, list, uuid):
        for i in list:
            if i[0] == uuid:
                return list.index(i)
        return -1

handler("0.0.1")
