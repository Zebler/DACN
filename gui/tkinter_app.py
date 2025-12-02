import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import json
from datetime import datetime

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
    sys.path.insert(0, application_path)
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.scheduler import PersonalScheduleAssistant
from src.storage.json_storage import JSONStorage


class ScheduleAssistantGUI:
    """Giao diện chính của ứng dụng"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Schedule Assistant")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize components
        self.assistant = PersonalScheduleAssistant()
        self.storage = JSONStorage()
        self.schedules = self.storage.load_all()
        
        # Setup UI
        self.setup_ui()
        self.load_schedules_to_table()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📅 PERSONAL SCHEDULE ASSISTANT",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== INPUT SECTION =====
        input_frame = tk.LabelFrame(
            main_frame,
            text="📝 Nhập văn bản tự do",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input text
        tk.Label(
            input_frame,
            text="Nhập lịch trình (VD: Họp nhóm 10 giờ sáng mai ở phòng 302):",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        self.input_text = tk.Entry(input_frame, font=("Arial", 11), width=70)
        self.input_text.pack(fill=tk.X, pady=(5, 10))
        self.input_text.bind('<Return>', lambda e: self.add_schedule())
        
        reminder_frame = tk.Frame(input_frame)
        reminder_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(
            reminder_frame,
            text="⏰ Nhắc nhở trước:",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Dropdown cho reminder time
        self.reminder_var = tk.StringVar(value="15")
        reminder_options = ["5", "10", "15", "30", "60", "120"]
        
        reminder_combo = ttk.Combobox(
            reminder_frame,
            textvariable=self.reminder_var,
            values=reminder_options,
            width=10,
            state="readonly",
            font=("Arial", 10)
        )
        reminder_combo.pack(side=tk.LEFT)
        
        tk.Label(
            reminder_frame,
            text="phút",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(5, 0))        

        # Buttons
        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        self.add_button = tk.Button(
            button_frame,
            text="➕ Thêm sự kiện",
            command=self.add_schedule,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🔍 Tìm kiếm",
            command=self.search_schedule,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="🗑️ Xóa",
            command=self.delete_schedule,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # ===== SCHEDULE LIST SECTION =====
        list_frame = tk.LabelFrame(
            main_frame,
            text="📋 Danh sách lịch trình",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ("ID", "Sự kiện", "Thời gian", "Địa điểm", "Nhắc nhở")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Sự kiện", text="Sự kiện")
        self.tree.heading("Thời gian", text="Thời gian")
        self.tree.heading("Địa điểm", text="Địa điểm")
        self.tree.heading("Nhắc nhở", text="Nhắc nhở (phút)")
        
        # Column widths
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Sự kiện", width=250)
        self.tree.column("Thời gian", width=180)
        self.tree.column("Địa điểm", width=180)
        self.tree.column("Nhắc nhở", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ===== STATUS BAR =====
        self.status_bar = tk.Label(
            self.root,
            text="Sẵn sàng",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def add_schedule(self):
        """Thêm sự kiện mới"""
        text = self.input_text.get().strip()
        
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung!")
            return
        
        # Process with NLP
        self.status_bar.config(text="Đang xử lý...")
        self.root.update()
        
        result = self.assistant.process(text)
        
        if result['success']:
            schedule = result['schedule']
            confidence = result.get('confidence', 0)
            
            # Save to storage
            schedule_id = self.storage.save(schedule)
            self.schedules = self.storage.load_all()
            
            # Update table
            self.load_schedules_to_table()
            
            # Clear input
            self.input_text.delete(0, tk.END)
            
            # Show success message
            self.status_bar.config(text=f"✅ Đã thêm: {schedule['event']} (Độ tin cậy: {confidence:.0f}%)")
            
            messagebox.showinfo(
                "Thành công",
                f"✅ Đã thêm lịch trình!\n\n"
                f"Sự kiện: {schedule['event']}\n"
                f"Thời gian: {self.format_datetime(schedule['start_time'])}\n"
                f"Địa điểm: {schedule.get('location', 'Không có')}\n"
                f"Độ tin cậy: {confidence:.0f}%"
            )
        else:
            errors = "\n".join(result['errors'])
            self.status_bar.config(text="❌ Lỗi xử lý")
            messagebox.showerror(
                "Lỗi",
                f"Không thể xử lý lịch trình!\n\n"
                f"Lỗi: {errors}\n\n"
                f"Vui lòng thử lại với format khác."
            )
    
    def delete_schedule(self):
        """Xóa sự kiện đã chọn"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sự kiện cần xóa!")
            return
        
        # Confirm
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sự kiện này?"):
            for item in selected:
                values = self.tree.item(item)['values']
                schedule_id = values[0]
                
                # Delete from storage
                self.storage.delete(schedule_id)
                self.schedules = self.storage.load_all()
            
            # Update table
            self.load_schedules_to_table()
            self.status_bar.config(text="🗑️ Đã xóa sự kiện")
    
    def search_schedule(self):
        """Tìm kiếm sự kiện"""
        search_window = tk.Toplevel(self.root)
        search_window.title("🔍 Tìm kiếm")
        search_window.geometry("400x150")
        search_window.resizable(False, False)
        
        tk.Label(
            search_window,
            text="Nhập từ khóa tìm kiếm:",
            font=("Arial", 10)
        ).pack(pady=(20, 5))
        
        search_entry = tk.Entry(search_window, font=("Arial", 11), width=40)
        search_entry.pack(pady=5)
        search_entry.focus()
        
        def do_search():
            keyword = search_entry.get().strip().lower()
            if not keyword:
                return
            
            # Clear current selection
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Search
            found = 0
            for schedule in self.schedules:
                if (keyword in schedule.get('event', '').lower() or
                    keyword in schedule.get('location', '').lower()):
                    self.insert_schedule_to_tree(schedule)
                    found += 1
            
            search_window.destroy()
            self.status_bar.config(text=f"🔍 Tìm thấy {found} kết quả")
        
        tk.Button(
            search_window,
            text="Tìm kiếm",
            command=do_search,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(pady=10)
        
        search_entry.bind('<Return>', lambda e: do_search())
    
    def load_schedules_to_table(self):
        """Load tất cả lịch trình vào bảng"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert schedules
        for schedule in self.schedules:
            self.insert_schedule_to_tree(schedule)
        
        self.status_bar.config(text=f"📊 Tổng: {len(self.schedules)} lịch trình")
    
    def insert_schedule_to_tree(self, schedule):
        """Insert một schedule vào tree"""
        self.tree.insert("", tk.END, values=(
            schedule.get('id', ''),
            schedule.get('event', ''),
            self.format_datetime(schedule.get('start_time', '')),
            schedule.get('location', ''),
            schedule.get('reminder_minutes', 15)
        ))
    
    def format_datetime(self, dt_str):
        """Format datetime string để hiển thị"""
        if not dt_str:
            return ""
        try:
            # Parse ISO format
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return dt_str


def main():
    """Main function"""
    root = tk.Tk()
    app = ScheduleAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()