import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient


# ---------------- DATABASE ----------------

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client["lost_found_db"]
except:
    messagebox.showerror("Error", "MongoDB not running!")
    exit()

found_collection = db["found"]
lost_collection = db["lost"]
matched_collection = db["matched"]
claimed_collection = db["claimed"]

# ---------------- USER SESSION ----------------

current_user = {"name": "", "reg": "", "is_admin": False}

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Lost & Found System")
root.geometry("1100x620")

# ---------------- BACKGROUND FUNCTION ----------------

def set_background(frame):
    try:
        bg = tk.PhotoImage(file=r"C:\Users\chris\dbms\bg.png")

        bg_label = tk.Label(frame, image=bg)
        bg_label.image = bg
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    except Exception as e:
        print("Background error:", e)
        frame.config(bg="#0f172a")

# ---------------- FUNCTIONS ----------------

def clear_fields():
    name_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    color_entry.delete(0, tk.END)

def show_status(msg):
    status_label.config(text=msg)

# ---------- MATCH ----------

def check_match(new_type, name, desc, color):
    query = {
        "name": name.lower(),
        "desc": desc.lower(),
        "color": color.lower()
    }

    if new_type == "found":
        match = lost_collection.find_one(query)
        if match:
            matched_collection.insert_one({
                **query,
                "status": "UNCLAIMED",
                "person_name": current_user["name"],
                "reg_no": current_user["reg"]
            })
            lost_collection.delete_one({"_id": match["_id"]})
            return True

    elif new_type == "lost":
        match = found_collection.find_one(query)
        if match:
            matched_collection.insert_one({
                **query,
                "status": "UNCLAIMED",
                "person_name": current_user["name"],
                "reg_no": current_user["reg"]
            })
            found_collection.delete_one({"_id": match["_id"]})
            return True

    return False

# ---------- ADD ----------

def add_found():
    name, desc, color = name_entry.get(), desc_entry.get(), color_entry.get()

    if not name or not desc or not color:
        messagebox.showwarning("Error", "All fields required")
        return

    if check_match("found", name, desc, color):
        show_status("Match Found! Merged")
    else:
        found_collection.insert_one({
            "name": name.lower(),
            "desc": desc.lower(),
            "color": color.lower(),
            "status": "FOUND",
            "person_name": current_user["name"],
            "reg_no": current_user["reg"]
        })
        show_status("Found Added")

    clear_fields()
    view_all()

def add_lost():
    name, desc, color = name_entry.get(), desc_entry.get(), color_entry.get()

    if not name or not desc or not color:
        messagebox.showwarning("Error", "All fields required")
        return

    if check_match("lost", name, desc, color):
        show_status("Match Found! Merged")
    else:
        lost_collection.insert_one({
            "name": name.lower(),
            "desc": desc.lower(),
            "color": color.lower(),
            "status": "LOST",
            "person_name": current_user["name"],
            "reg_no": current_user["reg"]
        })
        show_status("Lost Added")

    clear_fields()
    view_all()

# ---------- TREE SETUP ----------

def setup_tree(columns_list):
    global tree
    try:
        tree.destroy()
    except:
        pass

    tree = ttk.Treeview(content, columns=columns_list, show="headings")

    for col in columns_list:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

# ---------- VIEW ----------

def view_all():
    setup_tree(("S.No", "Person Name", "Reg No", "Item", "Description", "Color", "Status"))

    tree.delete(*tree.get_children())
    i = 1

    for col in [matched_collection, found_collection, lost_collection]:
        for item in col.find():
            tree.insert("", "end", values=(
                i,
                item.get("person_name"),
                item.get("reg_no"),
                item.get("name"),
                item.get("desc"),
                item.get("color"),
                item.get("status")
            ))
            i += 1

def view_claimed():
    setup_tree(("S.No", "Claimed By", "Claimed Reg", "Item", "Description", "Color", "Status"))

    tree.delete(*tree.get_children())
    i = 1

    for item in claimed_collection.find():
        tree.insert("", "end", values=(
            i,
            item.get("claimed_by"),
            item.get("claimed_reg"),
            item.get("name"),
            item.get("desc"),
            item.get("color"),
            "CLAIMED"
        ))
        i += 1

# ---------- CLAIM ----------

def claim_item():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Select item")
        return

    values = tree.item(selected, "values")
    query = {"name": values[3], "desc": values[4], "color": values[5]}

    item = matched_collection.find_one(query) or \
           found_collection.find_one(query) or \
           lost_collection.find_one(query)

    if not item:
        messagebox.showwarning("Error", "Item not found")
        return

    claimed_collection.insert_one({
        **query,
        "status": "CLAIMED",
        "claimed_by": current_user["name"],
        "claimed_reg": current_user["reg"]
    })

    matched_collection.delete_one(query)
    found_collection.delete_one(query)
    lost_collection.delete_one(query)

    show_status("Item Claimed")
    view_all()

# ---------- DELETE ----------

def delete_item():
    if not current_user["is_admin"]:
        messagebox.showerror("Access Denied", "Admin only")
        return

    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Select item")
        return

    values = tree.item(selected, "values")
    query = {"name": values[3], "desc": values[4], "color": values[5]}

    matched_collection.delete_one(query)
    found_collection.delete_one(query)
    lost_collection.delete_one(query)

    show_status("Item Deleted")
    view_all()

# ---------------- DASHBOARD ----------------
# (unchanged from your code)

def show_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    set_background(main_frame)

    def logout():
        current_user["name"] = ""
        current_user["reg"] = ""
        current_user["is_admin"] = False
        show_home()

    sidebar = tk.Frame(main_frame, bg="#020617", width=220)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="📦 Lost&Found",
             bg="#020617", fg="white",
             font=("Segoe UI", 14, "bold")).pack(pady=20)

    def side_btn(text, cmd):
        btn = tk.Label(sidebar, text=text,
                       bg="#020617", fg="#94a3b8",
                       font=("Segoe UI", 11),
                       padx=15, pady=10,
                       anchor="w", cursor="hand2")
        btn.pack(fill="x")
        btn.bind("<Button-1>", lambda e: cmd())

    side_btn("➕ Add Found", add_found)
    side_btn("📌 Add Lost", add_lost)
    side_btn("📋 View All", view_all)
    side_btn("✅ Claim Item", claim_item)
    side_btn("📦 Claimed Items", view_claimed)

    if current_user["is_admin"]:
        side_btn("🗑 Delete", delete_item)

    side_btn("🚪 Logout", logout)

    global content, name_entry, desc_entry, color_entry, status_label

    content = tk.Frame(main_frame, bg="#0f172a")
    content.pack(side="right", fill="both", expand=True)

    card = tk.Frame(content, bg="#1e293b")
    card.pack(padx=20, pady=10, fill="x")

    tk.Label(card, text="Item", bg="#1e293b", fg="white").grid(row=0, column=0, padx=10, pady=5)
    name_entry = ttk.Entry(card)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(card, text="Description", bg="#1e293b", fg="white").grid(row=1, column=0, padx=10, pady=5)
    desc_entry = ttk.Entry(card)
    desc_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(card, text="Color", bg="#1e293b", fg="white").grid(row=2, column=0, padx=10, pady=5)
    color_entry = ttk.Entry(card)
    color_entry.grid(row=2, column=1, padx=10, pady=5)

    status_label = tk.Label(content, text="Ready",
                            bg="#020617", fg="#94a3b8")
    status_label.pack(fill="x")

    view_all()

# ---------------- HOME (UPDATED UI) ----------------

def show_home():
    for widget in root.winfo_children():
        widget.destroy()

    home_frame = tk.Frame(root)
    home_frame.pack(fill="both", expand=True)

    set_background(home_frame)

    tk.Label(home_frame, text="LOST AND FOUND",
             font=("Segoe UI", 32, "bold"),
             fg="white", bg="#000000").pack(pady=40)

    # Center container
    center_frame = tk.Frame(home_frame, bg="#000000")
    center_frame.pack(expand=True)

    form = tk.Frame(center_frame, bg="#1e293b", padx=30, pady=25)
    form.pack()

    name_input = ttk.Entry(form, width=25)
    reg_input = ttk.Entry(form, width=25)

    tk.Label(form, text="Name", fg="white", bg="#1e293b")\
        .grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_input.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form, text="Register No", fg="white", bg="#1e293b")\
        .grid(row=1, column=0, padx=10, pady=10, sticky="w")
    reg_input.grid(row=1, column=1, padx=10, pady=10)

    def enter_user():
        if not name_input.get() or not reg_input.get():
            messagebox.showwarning("Error", "Enter details")
            return

        current_user["name"] = name_input.get()
        current_user["reg"] = reg_input.get()
        current_user["is_admin"] = False
        show_dashboard()

    ttk.Button(form, text="Enter", command=enter_user)\
        .grid(row=2, columnspan=2, pady=20)

    def admin_login():
        login_win = tk.Toplevel(root)
        login_win.title("Admin Login")
        login_win.geometry("300x200")

        user_entry = ttk.Entry(login_win)
        pass_entry = ttk.Entry(login_win, show="*")

        ttk.Label(login_win, text="Username").pack(pady=5)
        user_entry.pack(pady=5)

        ttk.Label(login_win, text="Password").pack(pady=5)
        pass_entry.pack(pady=5)

        def check():
            if user_entry.get() == "admin" and pass_entry.get() == "pass":
                current_user["is_admin"] = True
                login_win.destroy()
                show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        ttk.Button(login_win, text="Login", command=check).pack(pady=10)

    ttk.Button(home_frame, text="Admin Login", command=admin_login)\
        .pack(side="bottom", anchor="e", padx=20, pady=20)

# ---------------- START ----------------

show_home()
root.mainloop()