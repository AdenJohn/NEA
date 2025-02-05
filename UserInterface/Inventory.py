import ttkbootstrap as ttk 
from ttkbootstrap.constants import * 
from BasePage import BasePage

class InventoryPage(BasePage): 
    def __init__(self, parent, controller, *args, **kwargs): 
        super().__init__(parent, controller, *args, **kwargs)

        self.title_label = ttk.Label(self.main_frame, text="Inventory Manager", font=("Arial", 20))
        self.title_label.pack(pady=(20, 10))

        self.inventory_tree = ttk.Treeview(self.main_frame, columns=("Product ID", "SKU", "Product Name", "Price", "Stock"), show="headings")
        self.inventory_tree.heading("Product ID", text="ID")
        self.inventory_tree.heading("SKU", text="SKU")
        self.inventory_tree.heading("Product Name", text="Product Name")
        self.inventory_tree.heading("Price", text="Price")
        self.inventory_tree.heading("Stock", text="Stock Quantity")

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Product", command=lambda: self.add_product())
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Product", command=lambda: self.edit_product())
        self.edit_button.grid(row=1, column=0, padx=5, pady=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Product", command=lambda: self.delete_product())
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_inventory()

    def load_inventory(self):

        for item in self.inventory_tree.get_children(): 
            self.inventory_tree.delete(item)

            products = []

            if hasattr(self.controller, "inventory_manager"): 
                products = self.controller.inventory_manager.get_products()

            if products: 
                for product in products: 
                    self.inventory_tree.insert("", "end", values=(product.product_id, product.sku, product.product_name, product.price, product.stock_quantity))

            else: 
                messagebox.show_info("Info", "No products found")

    def add_product(self): 

        self.add_window = ttk.TopLevel(self)
        self.add_window.title("Add Product")

        ttk.Label(self.add_window, text="SKU: ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        sku_entry = ttk.Entry(self.add_window)
        sku_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_window, text="Product Name: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(self.add_window)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.add_window, text="Price: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        price_entry = ttk.Entry(self.add_window)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.add_window, text="Stock Quantity: ").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        quantity_entry = ttk.Entry(self.add_window)
        quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        def submit_add(): 
            sku = sku_entry.get().strip()
            product_name = name_entry.get().strip()

            try: 
                price = float(price_entry.get().strip())
            except ValueError: 
                Messagebox.show_error("Error", "Price must be a number")

        