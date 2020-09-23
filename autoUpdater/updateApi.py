from dashboard.models import PayerRemnant


class UpdateApi:
    def clearRemnant(self):
        remnants = PayerRemnant.objects.filter(has_remnant=True)
        for user in remnants:
            user.has_remnant = False
            user.save()