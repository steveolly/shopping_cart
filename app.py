
import tkinter as tk
from tkinter import messagebox


# =====================================================
# 1. SHOPPING CART LOGIC
# =====================================================

def add_item(cart, name, price, qty):
    for item in cart:
        if item["name"].lower() == name.lower():

            if item["price"] != price:
                return False

            item["qty"] += qty
            return True

    cart.append({
        "name": name,
        "price": price,
        "qty": qty
    })

    return True


def remove_item(cart, name):
    for i in range(len(cart)):
        if cart[i]["name"].lower() == name.lower():
            cart.pop(i)
            return True

    return False


def update_quantity(cart, name, new_qty):
    for item in cart:
        if item["name"].lower() == name.lower():
            item["qty"] = new_qty
            return True

    return False


def cart_total(cart):
    total = 0

    for item in cart:
        total += item["price"] * item["qty"]

    return total


def apply_discount(total, percent):
    return total - (total * percent / 100)


# =====================================================
# 2. APPLICATION DATA
# =====================================================

cart = []
current_discount = 0


# =====================================================
# 3. MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title("Stephen's Shopping Cart")
root.geometry("800x650")
root.minsize(500, 400)

root.configure(bg="#F1F5F9")


# =====================================================
# 4. SCROLLABLE APPLICATION CONTAINER
# =====================================================

main_canvas = tk.Canvas(
    root,
    bg="#F1F5F9",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

main_frame = tk.Frame(
    main_canvas,
    bg="#F1F5F9"
)

main_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def update_scroll_region(event=None):
    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


def resize_main_frame(event):
    main_canvas.itemconfigure(
        main_window,
        width=event.width
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)

main_canvas.bind(
    "<Configure>",
    resize_main_frame
)

main_canvas.configure(
    yscrollcommand=scrollbar.set
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =====================================================
# 5. MOUSE WHEEL SCROLLING
# =====================================================

def on_mousewheel(event):
    if event.delta:
        main_canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )


def on_linux_scroll_up(event):
    main_canvas.yview_scroll(-1, "units")


def on_linux_scroll_down(event):
    main_canvas.yview_scroll(1, "units")


root.bind_all("<MouseWheel>", on_mousewheel)
root.bind_all("<Button-4>", on_linux_scroll_up)
root.bind_all("<Button-5>", on_linux_scroll_down)


# =====================================================
# 6. UPDATE CART DISPLAY
# =====================================================

def update_cart_display():
    cart_display.delete(0, tk.END)

    for item in cart:
        item_total = item["price"] * item["qty"]

        cart_display.insert(
            tk.END,
            f'{item["name"]:<18} '
            f'₦{item["price"]:>10,.2f} '
            f'Qty: {item["qty"]:<4} '
            f'Total: ₦{item_total:,.2f}'
        )

    subtotal = cart_total(cart)

    discount_amount = subtotal * current_discount / 100

    final_total = apply_discount(
        subtotal,
        current_discount
    )

    subtotal_label.config(
        text=f"Subtotal: ₦{subtotal:,.2f}"
    )

    discount_amount_label.config(
        text=f"Discount: ₦{discount_amount:,.2f}"
    )

    final_total_label.config(
        text=f"FINAL TOTAL: ₦{final_total:,.2f}"
    )

    item_count = sum(
        item["qty"] for item in cart
    )

    count_label.config(
        text=f"Total Items: {item_count}"
    )


# =====================================================
# 7. CLEAR PRODUCT INPUTS
# =====================================================

def clear_product_inputs():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)


# =====================================================
# 8. ADD PRODUCT
# =====================================================

def on_add():
    name = name_entry.get().strip()
    price_text = price_entry.get().strip()
    qty_text = qty_entry.get().strip()

    if not name:
        messagebox.showerror(
            "Missing Product",
            "Please enter a product name."
        )
        name_entry.focus()
        return

    try:
        price = float(price_text)
        qty = int(qty_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Price must be a number and quantity must be a whole number."
        )
        return

    if price <= 0 or qty <= 0:
        messagebox.showerror(
            "Invalid Values",
            "Price and quantity must be greater than zero."
        )
        return

    if price != price or price == float("inf"):
        messagebox.showerror(
            "Invalid Price",
            "Please enter a valid price."
        )
        return

    success = add_item(
        cart,
        name,
        price,
        qty
    )

    if not success:
        messagebox.showerror(
            "Price Conflict",
            "This product already exists with a different price.\n"
            "Remove the existing product before adding it at another price."
        )
        return

    update_cart_display()
    clear_product_inputs()
    name_entry.focus()


# =====================================================
# 9. REMOVE SELECTED PRODUCT
# =====================================================

def on_remove():
    selected = cart_display.curselection()

    if not selected:
        messagebox.showerror(
            "No Selection",
            "Please select a product to remove."
        )
        return

    index = selected[0]
    name = cart[index]["name"]

    remove_item(cart, name)

    update_cart_display()


# =====================================================
# 10. UPDATE PRODUCT QUANTITY
# =====================================================

def on_update_quantity():
    selected = cart_display.curselection()

    if not selected:
        messagebox.showerror(
            "No Selection",
            "Please select a product first."
        )
        return

    try:
        new_qty = int(qty_entry.get().strip())

    except ValueError:
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a valid whole-number quantity."
        )
        return

    if new_qty <= 0:
        messagebox.showerror(
            "Invalid Quantity",
            "Quantity must be greater than zero."
        )
        return

    index = selected[0]
    name = cart[index]["name"]

    update_quantity(
        cart,
        name,
        new_qty
    )

    update_cart_display()
    qty_entry.delete(0, tk.END)


# =====================================================
# 11. APPLY DISCOUNT
# =====================================================

def on_apply_discount():
    global current_discount

    discount_text = discount_entry.get().strip()

    try:
        percent = float(discount_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Discount",
            "Please enter a valid discount percentage."
        )
        return

    if percent < 0 or percent > 100:
        messagebox.showerror(
            "Invalid Discount",
            "Discount must be between 0 and 100."
        )
        return

    if percent != percent or percent == float("inf"):
        messagebox.showerror(
            "Invalid Discount",
            "Please enter a valid discount."
        )
        return

    current_discount = percent

    update_cart_display()

    discount_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Discount Applied",
        f"{percent}% discount applied successfully!"
    )


# =====================================================
# 12. RESET DISCOUNT
# =====================================================

def on_reset_discount():
    global current_discount

    current_discount = 0

    update_cart_display()

    messagebox.showinfo(
        "Discount Reset",
        "The discount has been removed."
    )


# =====================================================
# 13. CLEAR CART
# =====================================================

def on_clear():
    global current_discount

    if not cart and current_discount == 0:
        clear_product_inputs()
        discount_entry.delete(0, tk.END)
        return

    confirm = messagebox.askyesno(
        "Clear Shopping Cart",
        "Are you sure you want to clear the entire cart?"
    )

    if not confirm:
        return

    cart.clear()
    current_discount = 0

    clear_product_inputs()
    discount_entry.delete(0, tk.END)

    update_cart_display()

    messagebox.showinfo(
        "Cart Cleared",
        "Your shopping cart has been reset."
    )


# =====================================================
# 14. SELECT PRODUCT FROM LIST
# =====================================================

def on_select_item(event):
    selected = cart_display.curselection()

    if not selected:
        return

    index = selected[0]
    item = cart[index]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, item["name"])

    price_entry.delete(0, tk.END)
    price_entry.insert(0, str(item["price"]))

    qty_entry.delete(0, tk.END)
    qty_entry.insert(0, str(item["qty"]))


# =====================================================
# 15. HEADER
# =====================================================

header = tk.Frame(
    main_frame,
    bg="#1E293B",
    height=90
)

header.pack(fill="x")

header.pack_propagate(False)

tk.Label(
    header,
    text="SHOPPING CART",
    font=("Arial", 23, "bold"),
    bg="#1E293B",
    fg="white"
).pack(pady=8)

tk.Label(
    header,
    text="Manage your products and calculate your purchases",
    font=("Arial", 10),
    bg="#1E293B",
    fg="#CBD5E1"
).pack()


# =====================================================
# 16. PRODUCT INPUT SECTION
# =====================================================

input_frame = tk.LabelFrame(
    main_frame,
    text="Product Information",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#1E293B",
    padx=15,
    pady=15
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=15
)


tk.Label(
    input_frame,
    text="Product Name",
    bg="white"
).grid(row=0, column=0, padx=10, pady=5, sticky="w")

name_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

name_entry.grid(row=1, column=0, padx=10, pady=5)


tk.Label(
    input_frame,
    text="Price (₦)",
    bg="white"
).grid(row=0, column=1, padx=10, pady=5, sticky="w")

price_entry = tk.Entry(
    input_frame,
    width=20,
    font=("Arial", 11)
)

price_entry.grid(row=1, column=1, padx=10, pady=5)


tk.Label(
    input_frame,
    text="Quantity",
    bg="white"
).grid(row=0, column=2, padx=10, pady=5, sticky="w")

qty_entry = tk.Entry(
    input_frame,
    width=15,
    font=("Arial", 11)
)

qty_entry.grid(row=1, column=2, padx=10, pady=5)


# =====================================================
# 17. PRODUCT BUTTONS
# =====================================================

button_frame = tk.Frame(
    main_frame,
    bg="#F1F5F9"
)

button_frame.pack(pady=5)


add_button = tk.Button(
    button_frame,
    text="ADD PRODUCT",
    command=on_add,
    width=18,
    bg="#16A34A",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat"
)

add_button.grid(row=0, column=0, padx=8)


remove_button = tk.Button(
    button_frame,
    text="REMOVE SELECTED",
    command=on_remove,
    width=18,
    bg="#DC2626",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat"
)

remove_button.grid(row=0, column=1, padx=8)


update_button = tk.Button(
    button_frame,
    text="UPDATE QUANTITY",
    command=on_update_quantity,
    width=18,
    bg="#2563EB",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat"
)

update_button.grid(row=0, column=2, padx=8)


# =====================================================
# 18. CART DISPLAY SECTION
# =====================================================

cart_frame = tk.LabelFrame(
    main_frame,
    text="Your Shopping Cart",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=10,
    pady=10
)

cart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


cart_display = tk.Listbox(
    cart_frame,
    width=100,
    height=12,
    font=("Courier New", 10),
    selectbackground="#2563EB",
    selectforeground="white"
)

cart_display.pack(
    fill="both",
    expand=True
)

cart_display.bind(
    "<<ListboxSelect>>",
    on_select_item
)


# =====================================================
# 19. ITEM COUNT
# =====================================================

count_label = tk.Label(
    main_frame,
    text="Total Items: 0",
    font=("Arial", 11, "bold"),
    bg="#F1F5F9",
    fg="#475569"
)

count_label.pack(pady=3)


# =====================================================
# 20. DISCOUNT SECTION
# =====================================================

discount_frame = tk.Frame(
    main_frame,
    bg="#F1F5F9"
)

discount_frame.pack(pady=8)


tk.Label(
    discount_frame,
    text="Discount (%):",
    font=("Arial", 11, "bold"),
    bg="#F1F5F9"
).grid(row=0, column=0, padx=8)


discount_entry = tk.Entry(
    discount_frame,
    width=12,
    font=("Arial", 11)
)

discount_entry.grid(row=0, column=1, padx=8)


discount_button = tk.Button(
    discount_frame,
    text="APPLY DISCOUNT",
    command=on_apply_discount,
    bg="#7C3AED",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat"
)

discount_button.grid(row=0, column=2, padx=8)


reset_discount_button = tk.Button(
    discount_frame,
    text="RESET DISCOUNT",
    command=on_reset_discount,
    bg="#64748B",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat"
)

reset_discount_button.grid(row=0, column=3, padx=8)


# =====================================================
# 21. TOTALS SECTION
# =====================================================

totals_frame = tk.Frame(
    main_frame,
    bg="white",
    padx=15,
    pady=10
)

totals_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


subtotal_label = tk.Label(
    totals_frame,
    text="Subtotal: ₦0.00",
    font=("Arial", 12),
    bg="white",
    fg="#334155"
)

subtotal_label.pack(anchor="e", pady=2)


discount_amount_label = tk.Label(
    totals_frame,
    text="Discount: ₦0.00",
    font=("Arial", 12),
    bg="white",
    fg="#DC2626"
)

discount_amount_label.pack(anchor="e", pady=2)


final_total_label = tk.Label(
    totals_frame,
    text="FINAL TOTAL: ₦0.00",
    font=("Arial", 17, "bold"),
    bg="white",
    fg="#15803D"
)

final_total_label.pack(anchor="e", pady=5)


# =====================================================
# 22. CLEAR CART BUTTON
# =====================================================

clear_button = tk.Button(
    main_frame,
    text="CLEAR / RESET CART",
    command=on_clear,
    width=25,
    bg="#1E293B",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat"
)

clear_button.pack(pady=12)


# =====================================================
# 23. KEYBOARD SHORTCUT
# =====================================================

root.bind(
    "<Return>",
    lambda event: on_add()
)


# =====================================================
# 24. START APPLICATION
# =====================================================

name_entry.focus()

root.mainloop()
