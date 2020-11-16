class handler():
    def __init__(self, version):
        self.version = version

    def result(self, skill, averageSkill, work, totalWork, **kwargs):
        return skill + ((int(averageSkill)/int(skill))*(((work*100)/totalWork)-20))

#[getUUID(ign), str(ctx.author), 100]
    def newSkill(self, profile, work, totalWork, **kwargs):
        return self.result(profile[2], profile[2], work, totalWork)

    def findProfile(self, list, uuid):
        for i in list:
            if i[0] == uuid:
                return list.index(i)
        return -1

handler("0.0.1")
