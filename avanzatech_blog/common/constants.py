class Status:
    ACTIVE = True
    INACTIVE = False

STATUS = {
    Status.ACTIVE: "resource is active",
    Status.INACTIVE: "resource is not active"
}

STATUS_CHOICES = [(status, description) for (status, description) in STATUS.items()]

