import React from "react";
import { InputText } from "../components/inputText";
import { Card } from "../components/Card";
import { useState } from "react";

const filtersList = [
  {
    id: 1,
    name: "Inteligência Artificial",
    selected: true,
  },
  {
    id: 2,
    name: "Workshop",
    selected: false,
  },
  {
    id: 3,
    name: "Palestra",
    selected: false,
  },
  {
    id: 4,
    name: "Intervista de Emprego",
    selected: false,
  },
  {
    id: 5,
    name: "Arquitetura",
    selected: false,
  },
];
const challenges = [
  {
    id: 1,
    title: "Desafio",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    company: "Empresa",
  },
  {
    id: 1,
    title: "Desafio",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    company: "Empresa",
  },
  {
    id: 1,
    title: "Desafio",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    company: "Empresa",
  },
  {
    id: 1,
    title: "Desafio",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    company: "Empresa",
  },
];

export const Desafios = () => {
  const [filters, setFilters] = useState(filtersList);
  const [desafios, setDesafios] = useState(challenges);

  return (
    <>
      <div className="bg-white w-full h-[60px]">Navbar</div>
      <div className="flex flex-col justify-center items-center mt-6">
        <div className=" text-white py-5 px-10 grid grid-cols-1 gap-5">
          {/* Desafios and description */}
          <div className="text-4xl text-left text-white font-bold">Desafios</div>
          <div className="text-sm text-white ">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod. Lorem ipsum dolor sit amet, consectetur adipiscing
            elit, sed do eiusmod
          </div>
          <div className="w-full grid grid-cols-1 gap-3">
            <div>
              <InputText
                placeholder={"Pesquisa"}
                className={"w-full rounded-xl"}
              />
              {/* adicionar icon to the input text? */}
              <button className="bg-brown-primary text-white p-2 px-4 text-sm rounded-full my-3">
                Limpar Filtros
              </button>
            </div>
            {/* Lista dos filtros */}
            <div className="w-full">
              {filters === undefined || filters === null ? (
                <div className="w-full text-gray-primary text-center">
                  No filters available. Please try again later.
                </div>
              ) : (
                <div className="flex flex-wrap">
                  {filters.map((filter) => (
                    <div className="p-1 my-1">
                      <button
                        key={filter.id}
                        className={`${
                          filter.selected
                            ? "bg-blue-primary text-white"
                            : "bad-outline text-black"
                        } p-2 px-3 text-sm rounded-full w-fit border border-white cursor-pointer`}
                      >
                        {filter.name}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="grid grid-cols-1 gap-6 p-4">
          {/* Desafios */}
          {desafios.map((challenge) => (
            <Card
              key={challenge.id}
              title={challenge.title}
              description={challenge.description}
              company={challenge.company}
              className={"p-4 rounded-xl bg-black-primary shadow-[0px_0px_16px_2px_#F1792455]"}
            />
          ))}
        </div>
      </div>
    </>
  );
};
