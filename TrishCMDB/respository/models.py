from django.db import models

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=128,verbose_name="资产名",unique=True)
    sn = models.CharField(max_length=128,verbose_name="SN序列号",unique=True)
    manufacturer = models.ForeignKey("Manufacturer")
    model = models.CharField(verbose_name="型号",max_length=64)
    purchase_date = models.DateField(blank=True,null=True)
    expire_date = models.DateField(blank=True,null=True)
    admin = models.ForeignKey("UserProfile")
    business_units = models.ForeignKey("BusinessUnit",blank=True)
    tags = models.ForeignKey("Tags",blank=True)
    cabinet = models.ForeignKey("DeviceCabinet")
    status_choices = (
        (0,'在线'),
        (1,'下线'),
        (2,'故障维护'),
        (3,'备用'),
        (4,'报废'),
        (5,'失联'),
    )
    status = models.SmallIntegerField(choices=status_choices)

class OS(models.Model):
    name = models.CharField(max_length=64)
    release = models.CharField(max_length=64)

class Server(models.Model):
    asset = models.OneToOneField("Asset")
    os = models.ForeignKey("OS")
    management_ip = models.GenericIPAddressField(blank=True,null=True)


class RAM(models.Model):
    """内存表"""
    asset = models.ForeignKey("Asset")
    sn = models.CharField(max_length=128)
    manufacturer = models.ForeignKey("Manufacturer")
    model = models.CharField(max_length=64)
    size = models.PositiveIntegerField("容量MB")
    slot = models.CharField("插槽",max_length=32)

    class Meta:
        unique_together = ("asset","slot")


class NIC(models.Model):
    """网卡表"""
    asset = models.ForeignKey("Asset")
    ip_addr = models.GenericIPAddressField(blank=True,null=True)
    mac = models.CharField(max_length=64,unique=True)


class Disk(models.Model):
    """硬盘"""
    asset = models.ForeignKey("Asset")
    sn = models.CharField(max_length=128)
    manufacturer = models.ForeignKey("Manufacturer")
    model = models.CharField(max_length=64)
    size = models.PositiveIntegerField("容量MB")
    slot = models.CharField("插槽", max_length=32)
    class Meta:
        unique_together = ("asset", "slot")

class CPU(models.Model):
    """CPU"""
    asset = models.OneToOneField("Asset")
    physical_num = models.PositiveSmallIntegerField("cpu物理个数")
    core_num = models.PositiveSmallIntegerField("cpu核数")
    model = models.CharField(max_length=64)


class NetworkDevice(models.Model):
    asset = models.OneToOneField("Asset")
    sub_asset_type_choices = ((0,'Switch'),(1,'Router'),(2,'FireWall'))
    sub_asset_type =  models.SmallIntegerField(choices=sub_asset_type_choices)
    management_ip = models.GenericIPAddressField(blank=True, null=True)


class StorageDevice(models.Model):
    asset = models.OneToOneField("Asset")
    management_ip = models.GenericIPAddressField(blank=True, null=True)


class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)
    contact = models.CharField(max_length=32)


class IDCFloor(models.Model):
    idc = models.ForeignKey("IDC")
    floor = models.CharField(max_length=32)

    class Meta:
        unique_together = ("idc","floor")


class DeviceCabinet(models.Model):
    """机柜"""
    floor = models.ForeignKey("IDCFloor")
    name =  models.CharField(max_length=32)

    class Meta:
        unique_together = ("floor", "name")

class BusinessUnit(models.Model):
    parent_unit  = models.ForeignKey("self",related_name="p_unit")
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("parent_unit", "name")

class Tags(models.Model):
    name = models.CharField(max_length=64,unique=True)

class Manufacturer(models.Model):
    name = models.CharField(max_length=64,unique=True)
