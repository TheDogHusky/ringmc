/**
 * 
 * @param {any} data form data
 * @returns {{valid: boolean, errors: string[]}} validation result
 */
function validateForm(data) {
    if (!data.title || data.title.trim() === '') {
        return { valid: false, errors: ['Le titre est requis.'] };
    }

    if (!data.content || data.content.trim() === '') {
        return { valid: false, errors: ['Le contenu est requis.'] };
    }

    if (data.prices) {
        try {
            const prices = JSON.parse(data.prices);
            if (!Array.isArray(prices)) {
                return { valid: false, errors: ['Les prix doivent être une liste.'] };
            }   
            for (const entry of prices) {
                if (typeof entry.item !== 'string' || typeof entry.value !== 'number') {
                    return { valid: false, errors: ['Chaque prix doit avoir un "item" de type chaîne et une "value" de type nombre.'] };
                }
            }
        } catch (e) {
            return { valid: false, errors: ['Les prix doivent être un JSON valide.'] };
        }
    }

    if (data.image_url && !/^https?:\/\/.+\.(jpg|jpeg|png|gif|webp)$/.test(data.image_url)) {
        return { valid: false, errors: ['L\'URL de l\'image doit être une URL valide pointant vers une image.'] };
    }

    if (data.category && data.category.trim() === '') {
        return { valid: false, errors: ['La catégorie ne peut pas être une chaîne vide.'] };
    }

    return { valid: true, errors: [] };
}

function postArticle(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = {
        title: formData.get('title'),
        content: formData.get('content'),   
        category: formData.get('category'),
        prices: formData.get('prices') || '[]',
        image_url: formData.get('image_url')
    };

    const result = validateForm(data);
    if (!result.valid) {
        alert('Erreur de validation :\n' + result.errors.join('\n'));
        return;
    }

    data.prices = JSON.parse(data.prices);

    fetch('/articles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            alert('Article publié avec succès !');
            form.reset();
        } else {
            alert('Erreur lors de la publication de l\'article.');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Erreur lors de la publication de l\'article.');
    });
}

function init_price_input(addBtn, list, prices) {
    addBtn.addEventListener('click', () => {
        const div = document.createElement('div');
        div.classList.add('price-entry');

        const itemInput = document.createElement('input');
        itemInput.type = 'text';
        itemInput.placeholder = 'Objet (ex: diamant)';
        itemInput.required = true;

        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.placeholder = 'Quantité';
        quantityInput.required = true;
        quantityInput.min = '1';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = '×';
        removeBtn.classList.add('btn', 'btn-danger');

        div.appendChild(itemInput);
        div.appendChild(quantityInput);
        div.appendChild(removeBtn);
        list.appendChild(div);
        prices.push({ item: '', value: 0 });

        function updatePrice() {
            const index = Array.from(list.children).indexOf(div);
            prices[index] = { item: itemInput.value, value: parseInt(quantityInput.value) || 0 };
        }

        removeBtn.addEventListener('click', () => {
            const index = Array.from(list.children).indexOf(div);
            prices.splice(index, 1);
            div.remove();
        });

        itemInput.addEventListener('input', updatePrice);
        quantityInput.addEventListener('input', updatePrice);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('article-form');
    const openModalButtons = document.querySelectorAll('.open-modal');

    const addPriceBtn = document.getElementById('add-price-btn');
    const pricesList = document.querySelector('.prices');
    let prices = [];
    
    init_price_input(addPriceBtn, pricesList, prices);

    openModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.getAttribute('data-target');
            const modal = document.querySelector(`[data-name="${target}"]`);
            if (modal) {
                modal.classList.add('active');
            }

            function closeModal() {
                modal.classList.remove('active');
            }

            const closeActions = modal.querySelectorAll('.close-modal');
            closeActions.forEach(action => {
                action.addEventListener('click', closeModal);
            });

            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    closeModal();
                }
            });
        });
    });

    form.addEventListener('submit', postArticle);
});