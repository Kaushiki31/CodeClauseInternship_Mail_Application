import tkinter as tk
from tkinter import messagebox, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class MailApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mail Application")

        self.setup_gui()

    def setup_gui(self):
        # Sender Email
        tk.Label(self.master, text="Sender Email:").grid(row=0, column=0, sticky=tk.W)
        self.sender_entry = tk.Entry(self.master)
        self.sender_entry.grid(row=0, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

        # Sender Password
        tk.Label(self.master, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

        # Recipient Email
        tk.Label(self.master, text="Recipient Email:").grid(row=2, column=0, sticky=tk.W)
        self.recipient_entry = tk.Entry(self.master)
        self.recipient_entry.grid(row=2, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

        # Subject
        tk.Label(self.master, text="Subject:").grid(row=3, column=0, sticky=tk.W)
        self.subject_entry = tk.Entry(self.master)
        self.subject_entry.grid(row=3, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

        # Message
        tk.Label(self.master, text="Message:").grid(row=4, column=0, sticky=tk.W)
        self.message_text = tk.Text(self.master, height=5, width=30)
        self.message_text.grid(row=4, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

        # Attach File Button
        attach_button = tk.Button(self.master, text="Attach File", command=self.attach_file)
        attach_button.grid(row=5, column=0, pady=10)

        # Send Button
        send_button = tk.Button(self.master, text="Send", command=self.send_email, bg="blue", fg="white", height=2, width=15)
        send_button.grid(row=5, column=1, pady=10)

        # Attached file path
        self.attached_file_path = ""

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attached_file_path = file_path
            messagebox.showinfo("File Attached", "File attached successfully.")

    def send_email(self):
        sender_email = self.sender_entry.get()
        sender_password = self.password_entry.get()
        recipient_email = self.recipient_entry.get()
        subject = self.subject_entry.get()
        message = self.message_text.get("1.0", tk.END)

        try:
            # Create a multipart message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            # Attach text message
            msg.attach(MIMEText(message))

            # Attach file if provided
            if self.attached_file_path:
                with open(self.attached_file_path, "rb") as attachment:
                    part = MIMEApplication(attachment.read(), Name="attachment")
                    part["Content-Disposition"] = f'attachment; filename="{self.attached_file_path}"'
                    msg.attach(part)

            # Create SMTP session
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)

                # Send email
                server.sendmail(sender_email, recipient_email, msg.as_string())

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MailApp(root)
    root.mainloop()
