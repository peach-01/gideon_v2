import psutil

class SystemMonitorTool:
    
    name = "system_monitor"
    
    def get_cpu_usage(self):
        return psutil.cpu_percent()
    

    def get_ram_usage(self):
        return psutil.virtual_memory().percent
    

    def get_disk_usage(self):
        return psutil.disk_usage("/").percent
    

    def get_battery(self):
        battery = psutil.sensors_battery()
        if not battery:
            return None
        
        return {
            "percent": battery.percent,
            "charging": battery.power_plugged,
        }
    
    
    def get_network(self):
        net = psutil.net_io_counters()

        return {
            "sent": net.bytes_sent,
            "received": net.bytes_recv,
        }
    

    def full_status(self):
        return {
            "cpu": self.get_cpu_usage(),
            "memory": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
            "battery": self.get_battery(),
            "network": self.get_network(),
        }