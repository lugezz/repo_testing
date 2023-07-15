

class TempItems(models.Model):
    scraper_task = models.ForeignKey(ScraperTask, on_delete=models.CASCADE, related_name='temp_items')