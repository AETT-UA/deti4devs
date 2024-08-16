import React, { useState, useEffect } from "react";
export const Desafios = () => {
    const [desafios, setDesafios] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetch("http://127.0.0.1:8000/desafios")
            .then((response) => response.json())
            .then((data) => {
                setDesafios(data);
                setLoading(false);
            });
    }, []);
    const handleAddDesafio = (event) => {
        event.preventDefault();
        const nome = event.target.nome.value;
        const pontos = event.target.pontos.value;
        const descricao = event.target.descricao.value;
        fetch("http://127.0.0.1:8000/desafios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nome, pontos, descricao }),
        })
            .then((response) => response.json())
            .then((data) => {
                setDesafios([...desafios, data]);
                event.target.reset();
            });
    };
    return (
        <>
            <h1 className="text-4xl font-semibold">Desafios</h1>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="table">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Nome</th>
                                <th>Pontos</th>
                                <th>Descrição</th>
                            </tr>
                        </thead>
                        {desafios.map((desafio) => (
                            <tr key={desafio.id}>
                                <td>{desafio.id}</td>
                                <td>{desafio.nome}</td>
                                <td>{desafio.pontos}</td>
                                <td>{desafio.descricao}</td>
                            </tr>
                        ))}
                    </table>
                </div>
            )}
            <form
                className="overflow-x-auto flex flex-col"
                onSubmit={handleAddDesafio}
            >
                <label>Nome</label>
                <input
                    className="input input-bordered w-full max-w-xs"
                    type="text"
                    name="nome"
                />
                <label>Pontos</label>
                <input
                    className="input input-bordered w-full max-w-xs"
                    type="number"
                    name="pontos"
                />
                <label>Descrição</label>
                <input
                    className="input input-bordered w-full max-w-xs"
                    type="text"
                    name="descricao"
                />
                <button type="submit" className="btn btn-primary max-w-xs mt-6">
                    Adicionar
                </button>
            </form>
        </>
    );
};
