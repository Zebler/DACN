import threading
import time
from datetime import datetime, timedelta
try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False
    print("Warning: plyer not installed. Notifications will be printed to console.")


class ReminderService:
    """Service để hiển thị pop-up nhắc nhở"""
    
    def __init__(self, storage):
        self.storage = storage
        self.running = False
        self.thread = None
        self.notified = set()  # Track đã nhắc nhở
    
    def start(self):
        """Bắt đầu service"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._check_reminders, daemon=True)
        self.thread.start()
        print("✅ Reminder service started")
    
    def stop(self):
        """Dừng service"""
        self.running = False
        print("⏹️ Reminder service stopped")
    
    def _check_reminders(self):
        """Kiểm tra và hiển thị nhắc nhở"""
        print("🔔 Reminder service is checking every 60 seconds...")
        
        while self.running:
            try:
                schedules = self.storage.load_all()
                current_time = datetime.now()
                
                for schedule in schedules:
                    schedule_id = schedule.get('id')
                    start_time_str = schedule.get('start_time')
                    
                    if not start_time_str or not schedule_id:
                        continue
                    
                    # Skip if already notified
                    if schedule_id in self.notified:
                        continue
                    
                    try:
                        # Parse start time
                        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                        
                        # Make timezone-naive for comparison
                        if start_time.tzinfo is not None:
                            start_time = start_time.replace(tzinfo=None)
                        
                        reminder_minutes = schedule.get('reminder_minutes', 15)
                        
                        # Tính thời gian nhắc nhở
                        reminder_time = start_time - timedelta(minutes=reminder_minutes)
                        time_diff = (reminder_time - current_time).total_seconds()
                        
                        # Nhắc nhở khi đến giờ (trong khoảng 60 giây)
                        if -60 <= time_diff <= 60:
                            self._show_notification(schedule)
                            self.notified.add(schedule_id)
                            print(f"🔔 Notified: {schedule['event']}")
                    
                    except Exception as e:
                        print(f"Lỗi xử lý schedule {schedule_id}: {e}")
            
            except Exception as e:
                print(f"Lỗi reminder loop: {e}")
            
            # Check mỗi 60 giây
            time.sleep(60)
    
    def _show_notification(self, schedule):
        """Hiển thị pop-up"""
        title = f"⏰ Nhắc nhở: {schedule['event']}"
        message = f"Thời gian: {self.format_time(schedule['start_time'])}\n"
        
        if schedule.get('location'):
            message += f"Địa điểm: {schedule['location']}"
        
        if HAS_PLYER:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name="Schedule Assistant",
                    timeout=10
                )
                print(f"✅ Notification shown: {title}")
            except Exception as e:
                print(f"❌ Lỗi notification: {e}")
                print(f"📢 {title}\n{message}")
        else:
            # Fallback: print to console
            print("\n" + "="*50)
            print(f"📢 {title}")
            print(message)
            print("="*50 + "\n")
    
    def format_time(self, dt_str):
        """Format datetime"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return dt_str