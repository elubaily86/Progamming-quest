const products = [
  {
    id: 1,
    name: "Кроссовки Nike Runner",
    category: "shoes",
    price: 42000,
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600"
  },
  {
    id: 2,
    name: "Кроссовки Adidas Sport",
    category: "shoes",
    price: 39000,
    image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600"
  },
  {
    id: 3,
    name: "Футбольный мяч Pro",
    category: "balls",
    price: 12500,
    image: "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?w=600"
  },
  {
    id: 4,
    name: "Баскетбольный мяч",
    category: "balls",
    price: 14500,
    image: "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600"
  },
  {
    id: 5,
    name: "Спортивная футболка",
    category: "clothes",
    price: 9000,
    image: "https://images.unsplash.com/photo-1523398002811-999ca8dec234?w=600"
  },
  {
    id: 6,
    name: "Спортивные шорты",
    category: "clothes",
    price: 8000,
    image: "https://images.unsplash.com/photo-1506629905607-d9f297d10015?w=600"
  },
  {
    id: 7,
    name: "Гантели 10 кг",
    category: "fitness",
    price: 22000,
    image: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600"
  },
  {
    id: 8,
    name: "Коврик для йоги",
    category: "fitness",
    price: 11000,
    image: "https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=600"
  }
];

function formatPrice(price) {
  return price.toLocaleString("ru-RU") + " ₸";
}

function getCart() {
  return JSON.parse(localStorage.getItem("sportCart")) || [];
}

function saveCart(cart) {
  localStorage.setItem("sportCart", JSON.stringify(cart));
}

function addToCart(id) {
  const product = products.find(item => item.id === id);
  if (!product) return;

  const cart = getCart();
  const existing = cart.find(item => item.id === id);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ ...product, quantity: 1 });
  }

  saveCart(cart);
  alert("Товар добавлен в корзину");
}

function renderProducts() {
  const container = document.getElementById("products");
  if (!container) return;

  const searchInput = document.getElementById("searchInput");
  const categoryFilter = document.getElementById("categoryFilter");

  const search = searchInput.value.toLowerCase();
  const category = categoryFilter.value;

  const filtered = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(search);
    const matchesCategory = category === "all" || product.category === category;
    return matchesSearch && matchesCategory;
  });

  container.innerHTML = filtered.map(product => `
    <div class="card">
      <img src="${product.image}" alt="${product.name}">
      <h3>${product.name}</h3>
      <p>Категория: ${categoryName(product.category)}</p>
      <div class="price">${formatPrice(product.price)}</div>
      <button class="btn" onclick="addToCart(${product.id})">Добавить в корзину</button>
    </div>
  `).join("");
}

function categoryName(category) {
  const names = {
    shoes: "Кроссовки",
    balls: "Мячи",
    clothes: "Одежда",
    fitness: "Фитнес"
  };
  return names[category] || category;
}

function renderCart() {
  const container = document.getElementById("cartItems");
  const totalElement = document.getElementById("total");
  if (!container || !totalElement) return;

  const cart = getCart();

  if (cart.length === 0) {
    container.innerHTML = "<p>Корзина пустая.</p>";
    totalElement.textContent = "Итого: 0 ₸";
    return;
  }

  container.innerHTML = cart.map(item => `
    <div class="cart-item">
      <div>
        <h3>${item.name}</h3>
        <p>${formatPrice(item.price)} × ${item.quantity}</p>
      </div>
      <button class="btn btn-secondary" onclick="removeFromCart(${item.id})">Удалить</button>
    </div>
  `).join("");

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  totalElement.textContent = "Итого: " + formatPrice(total);
}

function removeFromCart(id) {
  let cart = getCart();
  cart = cart.filter(item => item.id !== id);
  saveCart(cart);
  renderCart();
}

function clearCart() {
  localStorage.removeItem("sportCart");
  renderCart();
}

function checkout() {
  const cart = getCart();
  if (cart.length === 0) {
    alert("Корзина пустая");
    return;
  }

  alert("Заказ оформлен! Это демо-версия магазина.");
  clearCart();
}

document.addEventListener("DOMContentLoaded", () => {
  renderProducts();
  renderCart();

  const searchInput = document.getElementById("searchInput");
  const categoryFilter = document.getElementById("categoryFilter");

  if (searchInput) searchInput.addEventListener("input", renderProducts);
  if (categoryFilter) categoryFilter.addEventListener("change", renderProducts);
});
