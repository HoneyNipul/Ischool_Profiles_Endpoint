from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _
import uuid
from datetime import date, datetime
from django.core.validators import RegexValidator


def image_profile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile/{1}-{2}'.format(instance.creator_id, str(instance.id), filename)

class Profile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("na", "Prefer not to answer"),
    )

    PROFILE_TYPES = (
        ("faculty", "Faculty"),
        ("faculty_emeriti", "Faculty Emeriti"),
        ("faculty_ajunct", "Adjunct Faculty"),
        ("faculty_affiliated", "Affiliated Faculty"),
        ("staff", "Staff"),
        ("research_staff", "Research Staff"),
        ("doctoral_students", "Doctoral Students"),
        ("alumni", "Alumni"),
        ("student", "Student"),
        ("other", "Other"),
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    display_name = models.CharField(_("Display name"), blank=True, null=True, max_length=200)
    title = models.CharField(_("Title"), max_length=200, blank=True, null=True)
    biography = models.TextField(_("Biography"), blank=True, null=True)
    
    profile_type = models.CharField(_("Profile Type"), choices=PROFILE_TYPES, max_length=200, default="other", blank=True)
    profile_image = models.ImageField(_("Profile Image"), max_length=200, upload_to=image_profile_path, default=None, blank=True, null=True)
    media_data = JSONField(default=dict)
    date_of_birth = models.DateField(_("Birth Date"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=30, choices=GENDER_CHOICES, default="na", blank=True)
    suid = models.CharField(_("SUID"), max_length=15, blank=True, null=True)
    email_address = models.EmailField(_("Email Address"), blank=True, null=True)

    is_private = models.BooleanField(_("Privacy Status"), default=True)
    
    affiliations = models.ManyToManyField("Affiliation", related_name="profiles")
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    creator_id = models.CharField(_("Creator Id"), max_length=200)
    owner_id = models.CharField(_("Owner Id"), max_length=200, unique=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_id(self):
        return self.id

    def get_image_data():
        return self.profile_media_data

    def get_phone_numbers(self):
        pn_list = []
        for phone in self.phone_numbers.all():
            phone_number = {'phone type' : phone.phone_type, 'best time to contact' : phone.best_contact_time,
                             'number' : phone.number}
            pn_list.append(phone_number)
        return pn_list

    def get_addresses(self):
        ad_list = []
        for adr in self.addresses.all():
            address = {'street address' : adr.street_address, 'city' : adr.city,
                             'state' : adr.state, 'zip code' : adr.zip_code, 'country' : adr.country}
            ad_list.append(address)
        return ad_list

    
    def get_education(self):
        edu_list = []
        for edu in self.education.all():
            educate = {'university' : edu.university, 'gpa' : edu.gpa, 'degree' : edu.degree, 
                        'major' : edu.major, 'location' : edu.location, 'graduation_date' : edu.graduation_date}
            edu_list.append(educate)
        return edu_list
    
    def get_links(self):
        link_list = []
        for link in self.links.all():
            linkk = {'url_name' : link.url_name , 'url_link' : link.url_link}
            link_list.append(linkk)
        return link_list

    def get_attributes(self):
        attr_list = []
        for attr in self.attributes.all():
            attribute = {'title' : attr.title, 'value' : attr.value , 'sort_order' : attr.sort_order}
            attr_list.append(attribute)
        return attr_list

    def get_affiliations(self):
        aff_list = []
        for aff in self.affiliations.all():
            affiliation = {'id' : aff.id, 'name' : aff.name,
                            'academic rank' : aff.academic_rank,  
                            'AD group' : aff.associated_ad_group}
            aff_list.append(affiliation)
        return aff_list

    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class ProfilePhoneNumber(models.Model):
    profile = models.ForeignKey(Profile, related_name="phone_numbers", on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number format: '+999999999'.")
    number = models.CharField(_("Phone Number"), validators=[phone_regex], max_length=17, blank=True)
    phone_type = models.CharField(_("Phone Type"), max_length=100)
    best_contact_time = models.CharField(_("Best time to contact"), max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(_("Primary Number"), default=False)

class ProfileAddress(models.Model):
    profile = models.ForeignKey(Profile, related_name="addresses", on_delete=models.CASCADE)
    street_address = models.CharField(_("Street address"), max_length=200)
    city = models.CharField(_("City"), max_length=200)
    state = models.CharField(_("State"), max_length=50)
    zip_code = models.CharField(_("Zip Code"), max_length=11)
    country = models.CharField(_("Country"), max_length=50)
    address_type = models.CharField(_("Address Type"), max_length=100)

class ProfileEducation(models.Model):
    profile = models.ForeignKey(Profile, related_name="education",on_delete=models.CASCADE)
    university = models.CharField(_("University"), max_length=200, blank=True, null=True)
    gpa = models.DecimalField(_("GPA"), max_digits=2, decimal_places=1)
    degree = models.CharField(_("Degree"), max_length=200, blank=True, null=True)
    major = models.CharField(_("Major"), max_length=200)
    location = models.CharField(_("Location"), max_length=200, blank=True, null=True)
    graduation_date = models.DateField(_("Graduation Date"), blank=True, null=True)

class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, related_name="links", on_delete=models.CASCADE)
    url_name = models.CharField(_("URL Name"), max_length=200, blank=True, null=True)
    url_link = models.URLField(_("URL Link"), blank=True, null=True)

class ProfileAttribute(models.Model):
    profile = models.ForeignKey(Profile, related_name="attributes",on_delete=models.CASCADE)
    title = models.CharField(_("Attribute Title"), max_length=200, blank=True, null=True) #job title ?
    value = models.CharField(_("Attribute Value"), max_length=200, blank=True, null=True)
    sort_order = models.PositiveIntegerField(_("Sort Order"), default=0) #0 is not sorted

    def save(self, *args, **kwargs):
        if not self.sort_order:
            self.sort_order = self.profile.attributes.count()
        else:
            self._adjust_sort_order_for_other_attributes()
        
        super(ProfileAttribute, self).save(*args, **kwargs)

    def _adjust_sort_order_for_other_attributes(self):
        last_sort_order_number = 0
        for attribute in ProfileAttribute.objects.filter(profile=self.profile).order_by('sort_order'):
            last_sort_order_number = attribute.sort_order
        if last_sort_order_number <= self.profile.attributes.count():    
            for attribute in ProfileAttribute.objects.filter(profile=self.profile).order_by('sort_order'):
                if attribute.sort_order >= self.sort_order:
                    attribute.sort_order = attribute.sort_order + 1
                    attribute.save()    

class Affiliation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Display Name"), max_length=200)
    academic_rank = models.PositiveSmallIntegerField(_("Academic Weight"), default=0)
    associated_ad_group = models.CharField(_("AD Group"), max_length=200, blank=True, null=True)



