import tkinter as tk
from tkinter import messagebox


def validate_and_save(name: str, email: str, phone: str, amount: str) -> tuple[bool, str]:
    """Validate fields and append to donors.txt.

    Returns (success, message).
    """
    if not name or not email or not phone or not amount:
        return False, "All fields are required!"
    try:
        val = float(amount)
        if val <= 0:
            return False, "Donation amount must be greater than 0!"
    except ValueError:
        return False, "Donation amount must be a number!"
    # Basic email check
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address!"
    # Basic phone check (digits and optional +, -, spaces)
    digits = [c for c in phone if c.isdigit()]
    if len(digits) < 7:
        return False, "Please enter a valid phone number!"
    try:
        with open("donors.txt", "a", encoding="utf-8") as f:
            f.write(f"{name},{email},{phone},{amount}\n")
    except OSError as e:
        return False, f"Failed to save donor information: {e}"
    return True, "Donor information saved!"


def submit():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    amount = amount_var.get()
    ok, msg = validate_and_save(name, email, phone, amount)
    if not ok:
        messagebox.showerror("Error", msg)
        return
    messagebox.showinfo("Success", msg)
    name_var.set("")
    email_var.set("")
    phone_var.set("")
    amount_var.set("")


def run_gui():
    global name_var, email_var, phone_var, amount_var
    root = tk.Tk()
    root.title("Donor Information")

    tk.Label(root, text="Name:").grid(row=0, column=0, sticky="e")
    tk.Label(root, text="Email:").grid(row=1, column=0, sticky="e")
    tk.Label(root, text="Phone:").grid(row=2, column=0, sticky="e")
    tk.Label(root, text="Donation Amount:").grid(row=3, column=0, sticky="e")

    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()
    amount_var = tk.StringVar()

    tk.Entry(root, textvariable=name_var).grid(row=0, column=1)
    tk.Entry(root, textvariable=email_var).grid(row=1, column=1)
    tk.Entry(root, textvariable=phone_var).grid(row=2, column=1)
    tk.Entry(root, textvariable=amount_var).grid(row=3, column=1)

    tk.Button(root, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()


def run_cli():
    print("Running in CLI mode (no display detected). Enter donor information.")
    try:
        while True:
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            amount = input("Donation Amount: ").strip()
            ok, msg = validate_and_save(name, email, phone, amount)
            if ok:
                print("Success:", msg)
            else:
                print("Error:", msg)
            cont = input("Add another donor? [y/N]: ").strip().lower()
            if cont != "y":
                break
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")


def main():
    # Try to run GUI; if no display available, fall back to CLI.
    try:
        run_gui()
    except tk.TclError:
        run_cli()


if __name__ == "__main__":
    main()