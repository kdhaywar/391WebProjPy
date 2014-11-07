__author__ = 'hpabst'


class ProjImage(object):

    def __init__(self, imageFile=None, thumbnail=None, imageLocation=None, imageDate=None,
                 imageSubject=None, imagePrivacy=None, imageGroup=None, imageDesc=None,
                 ownerName=None, imageId=None):
        self.imageFile = imageFile #The actual bytes of the image.
        self.thumbnail = thumbnail #The bytes of the thumbnail.
        self.imageLocation = imageLocation #String describing the image's location.
        self.imageDate = imageDate #String of format mm/dd/yyyy to describe the image's date.
        self.imageSubject = imageSubject #String describing the format of the image.
        self.imagePrivacy = imagePrivacy #Int code for the privacy setting of the image. 1 for public, 0 for group,
                                         #2 for private.
        self.imageGroup = imageGroup #String describing the name of the group the image has security settings for.
        self.imageDesc = imageDesc #String giving the description of the image.
        self.ownerName = ownerName #String giving the username of the image's owner.
        self.imageId = imageId #Int giving the image's database generated ID.
        return