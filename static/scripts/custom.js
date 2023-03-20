//variables
let allContainerCart = document.querySelector('.products');   // Contenedor Producto
let containerBuyCart = document.querySelector('.card-items'); // Contenedor Compra
let priceTotal = document.querySelector('.price-total')       // Precio
let amountProduct = document.querySelector('.count-product'); // Contador

let buyThings = [];     // Arreglo de los Productos
let totalCard = 0;      // Variable Precio
let countProduct = 0;   // Variable del Contador

//Funciones 
loadEventListenrs();  // Agrupa todos los eventos de escucha
function loadEventListenrs(){
    allContainerCart.addEventListener('click', addProduct); // funcion agregar

    containerBuyCart.addEventListener('click', deleteProduct); // funcion eliminar
}

// Funcion Agregar Producto
function addProduct(e){ 
    e.preventDefault();
    if (e.target.classList.contains('btn-add-cart')) {
        const selectProduct = e.target.parentElement; 
        readTheContent(selectProduct); 
    }
}

function deleteProduct(e) {
    if (e.target.classList.contains('delete-product')) {
        const deleteId = e.target.getAttribute('data-id');
        // Recorremos el arreglo
        buyThings.forEach(value => {
            if (value.id == deleteId) { // Verificamos si hay mas de un producto
                let priceReduce = parseFloat(value.price) * parseFloat(value.amount);
                totalCard =  totalCard - priceReduce;
                totalCard = totalCard.toFixed(2);
            }
        });
        buyThings = buyThings.filter(product => product.id !== deleteId);
        
        countProduct--; // Resta Contador
    }
    //El contador se quedaba con "1" aun asi halla 0 productos
    if (buyThings.length === 0) {
        priceTotal.innerHTML = 0;
        amountProduct.innerHTML = 0;
    }
    loadHtml();
}

function readTheContent(product){
    const infoProduct = {
        image: product.querySelector('div img').src,            // Link de Imagen
        title: product.querySelector('.title').textContent,     // Link Titulo
        price: product.querySelector('div p span').textContent, // Link Precio
        id: product.querySelector('a').getAttribute('data-id'), // Link ID
        amount: 1                                               // Cantidad
    }

    totalCard = parseFloat(totalCard) + parseFloat(infoProduct.price);
    totalCard = totalCard.toFixed(2); // Se redondea el Float

    // Si existe se recorre el arreglo
    const exist = buyThings.some(product => product.id === infoProduct.id);
    if (exist) {
        const pro = buyThings.map(product => { // Nuevo Arreglo modificado el objeto
            if (product.id === infoProduct.id) {
                product.amount++; // Modifica el objeto y se aumenta el contador
                return product;
            } else {
                return product
            }
        });
        buyThings = [...pro];
    } else { // si no existe
        buyThings = [...buyThings, infoProduct] // Se crea un espacio y se concatena
        countProduct++; // Aumenta el contador
    }
    loadHtml();
}
// Funcion HTML para recorrer el objeto
function loadHtml(){
    clearHtml(); // Funcion Limpiar
    buyThings.forEach(product => {
        const {image, title, price, amount, id} = product; // Estructura de Objetos, Trae los atributos 
        const row = document.createElement('div');  // Creamos el Elementos
        row.classList.add('item');                  // Le Pasamos la clase
        //TemplateString `` copiamos toda la estructuta
        row.innerHTML = `                           
            <img src="${image}" alt="">
            <div class="item-content">
                <h5>${title}</h5>
                <h5 class="cart-price">${price}$</h5>
                <h6>Cantidad: ${amount}</h6>
            </div>
            <span class="delete-product" data-id="${id}">X</span>
        `;

        containerBuyCart.appendChild(row); // Pasamo los datos al contenedor

        priceTotal.innerHTML = totalCard;  // Mostramos el Valor Total

        amountProduct.innerHTML = countProduct;
    });
}
 function clearHtml(){
    containerBuyCart.innerHTML = ''; 
 }