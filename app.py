
from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
import json
import resend

app = Flask(__name__)

# =========================================================
# PRODUCTS
# =========================================================

PRODUCTS = [
    {
        "id": 1,
        "name": "1.8 GB RAM",
        "price": 3000,
        "category": "RAM",
        "description": "1.8 GB laptop RAM",
        "image": "ram.jfif"
    },
    {
        "id": 2,
        "name": "Dell Keyboard + Mouse Combo",
        "price": 1000,
        "category": "Keyboard & Mouse",
        "description": "Dell keyboard and mouse combo",
        "image": "dell_combo.jfif"
    },
    {
        "id": 3,
        "name": "HS04 Battery",
        "price": 700,
        "category": "Battery",
        "description": "HS04 laptop battery",
        "image": "hs04_battery.jfif"
    },
    {
        "id": 4,
        "name": "256 GB SSD",
        "price": 2000,
        "category": "SSD",
        "description": "256 GB laptop SSD",
        "image": "ssd_256gb.jfif"
    },
    {
        "id": 5,
        "name": "Laptop Screen",
        "price": 5000,
        "category": "Screen",
        "description": "Laptop replacement screen",
        "image": "laptop_screen.jfif"
    },
    {
        "id": 6,
        "name": "Laptop Panel",
        "price": 700,
        "category": "Panel",
        "description": "Laptop replacement panel",
        "image": "laptop_panel.jfif"
    },
    {
        "id": 7,
        "name": "Laptop Touchpad",
        "price": 700,
        "category": "Touchpad",
        "description": "Laptop replacement touchpad",
        "image": "laptop_touchpad.jfif"
    }
]


# =========================================================
# EMAIL SETTINGS
# =========================================================

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")

BUSINESS_EMAIL = "harishpurohit517@gmail.com"

# For Resend testing.
# Later you can replace this with a sender from your
# verified domain.
SENDER_EMAIL = os.environ.get(
    "SENDER_EMAIL",
    "onboarding@resend.dev"
)

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


# =========================================================
# PRODUCT IMAGE ROUTE
# =========================================================

@app.route("/product-image/<path:filename>")
def product_image(filename):

    folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    return send_from_directory(
        folder,
        filename
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    products_json = json.dumps(PRODUCTS)

    html = """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>VASUDEV TECHNOLOGIES</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f6f8;
    color: #111827;
}


/* HEADER */

header {
    background: #0b1220;
    color: white;
    padding: 18px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 1px;
}

.cart-button {
    border: none;
    background: #2563eb;
    color: white;
    padding: 11px 18px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 15px;
}

.cart-button:hover {
    background: #1d4ed8;
}


/* HERO */

.hero {
    background:
        linear-gradient(
            135deg,
            #0f172a,
            #1e40af
        );

    color: white;
    text-align: center;
    padding: 75px 20px;
}

.hero h1 {
    font-size: 44px;
    margin: 0 0 12px;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
}


/* SEARCH */

.search-area {
    text-align: center;
    padding: 28px 20px 10px;
}

.search-box {
    width: 90%;
    max-width: 650px;
    padding: 15px 20px;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    font-size: 16px;
    outline: none;
}


/* PRODUCTS */

.products {
    max-width: 1250px;
    margin: auto;
    padding: 25px 20px 50px;

    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(240px, 1fr)
        );

    gap: 25px;
}

.card {
    background: white;
    border-radius: 18px;
    overflow: hidden;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.08);

    transition: 0.25s;
}

.card:hover {
    transform: translateY(-5px);
}

.product-image {
    width: 100%;
    height: 210px;
    object-fit: contain;
    padding: 15px;
    background: white;
}

.card-content {
    padding: 18px;
}

.category {
    color: #2563eb;
    font-size: 13px;
    font-weight: bold;
}

.card h2 {
    font-size: 20px;
    margin: 8px 0;
}

.description {
    color: #6b7280;
    font-size: 14px;
    min-height: 40px;
}

.price {
    font-size: 23px;
    font-weight: bold;
    margin: 15px 0;
}

.add-button {
    width: 100%;
    border: none;
    background: #111827;
    color: white;
    padding: 13px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
}

.add-button:hover {
    background: #2563eb;
}


/* OVERLAY */

.overlay {
    display: none;

    position: fixed;

    inset: 0;

    background:
        rgba(0, 0, 0, 0.55);

    z-index: 2000;
}


/* CART */

.cart-panel {
    background: white;

    width: 95%;
    max-width: 520px;

    height: 100%;

    position: absolute;

    right: 0;
    top: 0;

    padding: 25px;

    overflow-y: auto;
}

.cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close-button {
    border: none;
    background: #ef4444;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
}

.cart-item {
    border-bottom: 1px solid #e5e7eb;
    padding: 15px 0;
}

.cart-item-name {
    font-weight: bold;
    font-size: 17px;
}

.quantity {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.quantity button {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 6px;
    background: #e5e7eb;
    cursor: pointer;
}

.quantity .remove {
    width: auto;
    padding: 0 12px;
    color: #dc2626;
    background: #fee2e2;
}

.total {
    font-size: 23px;
    font-weight: bold;
    margin: 25px 0;
}

.enquire-button {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 10px;
    background: #16a34a;
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

.enquire-button:hover {
    background: #15803d;
}


/* ENQUIRY MODAL */

.modal {
    display: none;

    position: fixed;

    inset: 0;

    background:
        rgba(0, 0, 0, 0.65);

    z-index: 3000;

    justify-content: center;
    align-items: center;

    padding: 20px;
}

.form-box {
    background: white;

    width: 100%;
    max-width: 450px;

    border-radius: 18px;

    padding: 30px;
}

.form-box h2 {
    margin-top: 0;
}

.form-box input {
    width: 100%;

    padding: 14px;

    margin:
        8px 0 15px;

    border:
        1px solid #d1d5db;

    border-radius: 9px;

    font-size: 16px;
}

.submit-button {
    width: 100%;

    padding: 14px;

    background: #2563eb;

    color: white;

    border: none;

    border-radius: 9px;

    font-weight: bold;

    cursor: pointer;
}

.cancel-button {
    width: 100%;

    padding: 12px;

    margin-top: 8px;

    background: #e5e7eb;

    border: none;

    border-radius: 9px;

    cursor: pointer;
}

.message {
    margin-top: 15px;

    padding: 12px;

    border-radius: 8px;

    display: none;
}

.success {
    background: #dcfce7;
    color: #166534;
}

.error {
    background: #fee2e2;
    color: #991b1b;
}


/* FOOTER */

footer {
    background: #0b1220;

    color: white;

    text-align: center;

    padding: 35px;

    margin-top: 20px;
}


/* MOBILE */

@media (max-width: 600px) {

    .hero h1 {
        font-size: 32px;
    }

    .logo {
        font-size: 18px;
    }

    .cart-panel {
        width: 100%;
    }

}

</style>

</head>


<body>


<header>

<div class="logo">
VASUDEV TECHNOLOGIES
</div>

<button
    class="cart-button"
    onclick="openCart()"
>
🛒 Cart (<span id="cartCount">0</span>)
</button>

</header>


<section class="hero">

<h1>
VASUDEV TECHNOLOGIES
</h1>

<p>
Laptop Parts • Computer Accessories • Quality Products
</p>

</section>


<div class="search-area">

<input
    class="search-box"
    id="searchBox"
    type="text"
    placeholder="Search products..."
    oninput="searchProducts()"
>

</div>


<div
    class="products"
    id="productsContainer"
></div>


<footer>

<h2>
VASUDEV TECHNOLOGIES
</h2>

<p>
Quality laptop parts and computer accessories.
</p>

<p>
© 2026 VASUDEV TECHNOLOGIES
</p>

</footer>


<!-- CART -->

<div
    class="overlay"
    id="cartOverlay"
>

<div class="cart-panel">

<div class="cart-header">

<h2>
🛒 Your Cart
</h2>

<button
    class="close-button"
    onclick="closeCart()"
>
Close
</button>

</div>


<div id="cartItems"></div>


<div class="total">

Total:
₹<span id="cartTotal">0</span>

</div>


<button
    class="enquire-button"
    onclick="openEnquiry()"
>
Enquire About These Products
</button>


</div>

</div>


<!-- ENQUIRY FORM -->

<div
    class="modal"
    id="enquiryModal"
>

<div class="form-box">

<h2>
Customer Enquiry
</h2>

<p>
Enter your details and we will contact you.
</p>


<label>
Name
</label>

<input
    id="customerName"
    type="text"
    placeholder="Your name"
>


<label>
Phone Number
</label>

<input
    id="customerPhone"
    type="tel"
    placeholder="Your phone number"
>


<button
    class="submit-button"
    onclick="submitEnquiry()"
>
Send Enquiry
</button>


<button
    class="cancel-button"
    onclick="closeEnquiry()"
>
Cancel
</button>


<div
    id="message"
    class="message"
></div>


</div>

</div>


<script>

const products = PRODUCTS_DATA;

let cart = [];


/* ======================================================
   DISPLAY PRODUCTS
====================================================== */

function displayProducts(list) {

    const container =
        document.getElementById(
            "productsContainer"
        );

    container.innerHTML = "";


    if (list.length === 0) {

        container.innerHTML = `
            <p style="
                grid-column:1/-1;
                text-align:center;
                font-size:18px;
            ">
                No products found.
            </p>
        `;

        return;
    }


    list.forEach(function(product) {

        container.innerHTML += `

        <div class="card">

            <img
                class="product-image"
                src="/product-image/${product.image}"
                alt="${product.name}"
                onerror="this.style.display='none'"
            >

            <div class="card-content">

                <div class="category">
                    ${product.category}
                </div>

                <h2>
                    ${product.name}
                </h2>

                <div class="description">
                    ${product.description}
                </div>

                <div class="price">
                    ₹${product.price.toLocaleString("en-IN")}
                </div>

                <button
                    class="add-button"
                    onclick="addToCart(${product.id})"
                >
                    Add to Cart
                </button>

            </div>

        </div>

        `;

    });

}


/* ======================================================
   ADD TO CART
====================================================== */

function addToCart(id) {

    const existing =
        cart.find(function(item) {

            return item.id === id;

        });


    if (existing) {

        existing.quantity++;

    }

    else {

        const product =
            products.find(function(item) {

                return item.id === id;

            });


        if (!product) {
            return;
        }


        cart.push({

            id: product.id,

            name: product.name,

            price: product.price,

            category: product.category,

            quantity: 1

        });

    }


    updateCart();

}


/* ======================================================
   INCREASE
====================================================== */

function increaseQuantity(id) {

    const item =
        cart.find(function(product) {

            return product.id === id;

        });


    if (item) {

        item.quantity++;

    }


    updateCart();

}


/* ======================================================
   DECREASE
====================================================== */

function decreaseQuantity(id) {

    const item =
        cart.find(function(product) {

            return product.id === id;

        });


    if (!item) {
        return;
    }


    item.quantity--;


    if (item.quantity <= 0) {

        cart =
            cart.filter(function(product) {

                return product.id !== id;

            });

    }


    updateCart();

}


/* ======================================================
   REMOVE
====================================================== */

function removeFromCart(id) {

    cart =
        cart.filter(function(product) {

            return product.id !== id;

        });


    updateCart();

}


/* ======================================================
   UPDATE CART
====================================================== */

function updateCart() {

    const count =
        cart.reduce(
            function(total, item) {

                return total + item.quantity;

            },
            0
        );


    document.getElementById(
        "cartCount"
    ).innerText = count;


    const container =
        document.getElementById(
            "cartItems"
        );


    container.innerHTML = "";


    let total = 0;


    if (cart.length === 0) {

        container.innerHTML = `
            <p>Your cart is empty.</p>
        `;

    }


    cart.forEach(function(item) {

        const subtotal =
            item.price * item.quantity;


        total += subtotal;


        container.innerHTML += `

        <div class="cart-item">

            <div class="cart-item-name">
                ${item.name}
            </div>

            <div>
                ₹${item.price.toLocaleString("en-IN")}
                × ${item.quantity}
            </div>

            <div>
                Subtotal:
                ₹${subtotal.toLocaleString("en-IN")}
            </div>

            <div class="quantity">

                <button
                    onclick="decreaseQuantity(${item.id})"
                >
                    −
                </button>

                <span>
                    ${item.quantity}
                </span>

                <button
                    onclick="increaseQuantity(${item.id})"
                >
                    +
                </button>

                <button
                    class="remove"
                    onclick="removeFromCart(${item.id})"
                >
                    Remove
                </button>

            </div>

        </div>

        `;

    });


    document.getElementById(
        "cartTotal"
    ).innerText =
        total.toLocaleString("en-IN");

}


/* ======================================================
   OPEN CART
====================================================== */

function openCart() {

    document.getElementById(
        "cartOverlay"
    ).style.display = "block";

}


/* ======================================================
   CLOSE CART
====================================================== */

function closeCart() {

    document.getElementById(
        "cartOverlay"
    ).style.display = "none";

}


/* ======================================================
   OPEN ENQUIRY
====================================================== */

function openEnquiry() {

    if (cart.length === 0) {

        alert(
            "Please add at least one product to the cart."
        );

        return;
    }


    document.getElementById(
        "enquiryModal"
    ).style.display = "flex";

}


/* ======================================================
   CLOSE ENQUIRY
====================================================== */

function closeEnquiry() {

    document.getElementById(
        "enquiryModal"
    ).style.display = "none";

}


/* ======================================================
   MESSAGE
====================================================== */

function showMessage(text, success) {

    const message =
        document.getElementById(
            "message"
        );


    message.style.display = "block";


    if (success) {

        message.className =
            "message success";

    }

    else {

        message.className =
            "message error";

    }


    message.innerText = text;

}


/* ======================================================
   SEND ENQUIRY
====================================================== */

function submitEnquiry() {

    const name =
        document.getElementById(
            "customerName"
        ).value.trim();


    const phone =
        document.getElementById(
            "customerPhone"
        ).value.trim();


    if (!name) {

        showMessage(
            "Please enter your name.",
            false
        );

        return;
    }


    if (!phone) {

        showMessage(
            "Please enter your phone number.",
            false
        );

        return;
    }


    if (cart.length === 0) {

        showMessage(
            "Your cart is empty.",
            false
        );

        return;
    }


    showMessage(
        "Sending enquiry...",
        true
    );


    fetch(
        "/enquiry",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                name: name,

                phone: phone,

                cart: cart.map(
                    function(item) {

                        return {

                            id: item.id,

                            quantity:
                                item.quantity

                        };

                    }
                )

            })

        }
    )

    .then(function(response) {

        return response.json();

    })

    .then(function(data) {

        if (data.success) {

            showMessage(
                "✅ Enquiry sent successfully!",
                true
            );


            cart = [];


            updateCart();


            setTimeout(
                function() {

                    closeEnquiry();

                    closeCart();


                    document.getElementById(
                        "customerName"
                    ).value = "";


                    document.getElementById(
                        "customerPhone"
                    ).value = "";


                    document.getElementById(
                        "message"
                    ).style.display = "none";

                },
                1800
            );

        }

        else {

            showMessage(
                data.error ||
                "Could not send enquiry.",
                false
            );

        }

    })

    .catch(function(error) {

        console.error(error);


        showMessage(
            "Could not connect to the server.",
            false
        );

    });

}


/* ======================================================
   SEARCH
====================================================== */

function searchProducts() {

    const query =
        document.getElementById(
            "searchBox"
        ).value
        .toLowerCase()
        .trim();


    const filtered =
        products.filter(
            function(product) {

                return (

                    product.name
                        .toLowerCase()
                        .includes(query)

                    ||

                    product.category
                        .toLowerCase()
                        .includes(query)

                    ||

                    product.description
                        .toLowerCase()
                        .includes(query)

                );

            }
        );


    displayProducts(filtered);

}


/* ======================================================
   START
====================================================== */

displayProducts(products);

updateCart();

</script>


</body>

</html>
"""

    html = html.replace(
        "PRODUCTS_DATA",
        products_json
    )

    return render_template_string(html)


# =========================================================
# ENQUIRY API
# =========================================================

@app.route("/enquiry", methods=["POST"])
def enquiry():

    try:

        data = request.get_json(silent=True)


        if not data:

            return jsonify({
                "success": False,
                "error": "Invalid request."
            }), 400


        name = str(
            data.get("name", "")
        ).strip()


        phone = str(
            data.get("phone", "")
        ).strip()


        cart = data.get(
            "cart",
            []
        )


        if not name:

            return jsonify({
                "success": False,
                "error": "Please enter your name."
            }), 400


        if not phone:

            return jsonify({
                "success": False,
                "error": "Please enter your phone number."
            }), 400


        if not isinstance(cart, list) or not cart:

            return jsonify({
                "success": False,
                "error": "Cart is empty."
            }), 400


        # -------------------------------------------------
        # BUILD PRODUCT LIST
        # -------------------------------------------------

        rows = []

        total = 0


        for item in cart:

            try:

                product_id = int(
                    item.get("id")
                )

                quantity = int(
                    item.get("quantity", 1)
                )

            except (TypeError, ValueError):

                continue


            if quantity <= 0:

                continue


            product = next(
                (
                    product
                    for product in PRODUCTS
                    if product["id"] == product_id
                ),
                None
            )


            if product is None:

                continue


            subtotal = (
                product["price"] *
                quantity
            )


            total += subtotal


            rows.append(
                f"""
                <tr>

                    <td style="
                        padding:10px;
                        border:1px solid #ddd;
                    ">
                        {product["name"]}
                    </td>

                    <td style="
                        padding:10px;
                        border:1px solid #ddd;
                    ">
                        {quantity}
                    </td>

                    <td style="
                        padding:10px;
                        border:1px solid #ddd;
                    ">
                        ₹{product["price"]:,}
                    </td>

                    <td style="
                        padding:10px;
                        border:1px solid #ddd;
                    ">
                        ₹{subtotal:,}
                    </td>

                </tr>
                """
            )


        if not rows:

            return jsonify({
                "success": False,
                "error": "No valid products found."
            }), 400


        product_rows = "".join(rows)


        # -------------------------------------------------
        # EMAIL
        # -------------------------------------------------

        email_html = f"""

        <div style="
            font-family:Arial,sans-serif;
            max-width:800px;
        ">

            <h1 style="
                color:#1e3a8a;
            ">
                VASUDEV TECHNOLOGIES
            </h1>

            <h2>
                New Customer Enquiry
            </h2>

            <hr>

            <h3>
                Customer Details
            </h3>

            <p>
                <strong>Name:</strong>
                {name}
            </p>

            <p>
                <strong>Phone:</strong>
                {phone}
            </p>

            <h3>
                Products Enquired
            </h3>

            <table style="
                border-collapse:collapse;
                width:100%;
            ">

                <thead>

                    <tr>

                        <th style="
                            padding:10px;
                            border:1px solid #ddd;
                        ">
                            Product
                        </th>

                        <th style="
                            padding:10px;
                            border:1px solid #ddd;
                        ">
                            Quantity
                        </th>

                        <th style="
                            padding:10px;
                            border:1px solid #ddd;
                        ">
                            Price
                        </th>

                        <th style="
                            padding:10px;
                            border:1px solid #ddd;
                        ">
                            Subtotal
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {product_rows}

                </tbody>

            </table>

            <h2>
                Total: ₹{total:,}
            </h2>

            <hr>

            <p>
                This enquiry was submitted through
                the VASUDEV TECHNOLOGIES website.
            </p>

        </div>

        """


        # -------------------------------------------------
        # RESEND CHECK
        # -------------------------------------------------

        if not RESEND_API_KEY:

            print(
                "ERROR: RESEND_API_KEY is missing."
            )

            return jsonify({
                "success": False,
                "error": "Email system is not configured."
            }), 500


        # -------------------------------------------------
        # SEND EMAIL
        # -------------------------------------------------

        print(
            "Sending enquiry through Resend..."
        )


        params = {
            "from": SENDER_EMAIL,
            "to": [BUSINESS_EMAIL],
            "subject":
                f"New VASUDEV Enquiry - {name}",
            "html": email_html
        }


        result = resend.Emails.send(
            params
        )


        print(
            "Resend email result:",
            result
        )


        return jsonify({
            "success": True,
            "message":
                "Enquiry sent successfully."
        })


    except Exception as error:

        print(
            "RESEND EMAIL ERROR:"
        )

        print(
            str(error)
        )


        return jsonify({
            "success": False,
            "error":
                "Email could not be sent. Please try again."
        }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

