import React, { useState } from 'react';

function AddProduto() {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [quantity, setQuantity] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/produto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, price, quantity })
        });
        const data = await response.json();
        setMessage(data.message);
    };

    return (
        <div>
            <h2>Adicionar Produto</h2>
            <form onSubmit={handleSubmit}>
                <label>Nome:</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
                <label>Preço:</label>
                <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
                <label>Quantidade:</label>
                <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
                <button type="submit">Adicionar</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default AddProduto;