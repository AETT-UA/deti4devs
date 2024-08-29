import BaseLayout from "../components/BaseLayout";

export default function Profile() {
  return (
    <BaseLayout>
      <div className="h-fit w-full px-5 mt-3">
        <div className="text-4xl text-white font-semibold">Perfil</div>
        <div className="w-full h-fit mt-4">
          <div className="text-2xl text-white">Código QR</div>
          <div className="px-5 w-full h-36 mt-3 rounded-lg bg-[#2a2a2a] flex flex-row justify-between items-center">
            <div className="w-24 h-24 rounded-lg bg-white"></div>
            <button className="btn btn-outline rounded-3xl px-5">
              Expandir
            </button>
          </div>
        </div>
        <div className="w-full h-fit mt-4">
          <div className="text-2xl text-white font-semibold">Pontos</div>
          <div className="px-5 w-full h-36 mt-3 rounded-lg flex flex-row justify-between items-center">
            <div className="w-1/2 h-full flex items-center flex-col justify-center">
              <div className="text-4xl text-white font-semibold">34</div>
              <div className="text-sm text-white">Pontos</div>
            </div>
            <div className="w-1/2 h-fit">
              <div className="h-full mx-auto w-fit">
                <div className="text-lg text-white font-semibold">Pontos</div>
                <div className="text-sm text-green-300">#13</div>
                <div className="text-lg text-white font-semibold mt-3">
                  Desafios
                </div>
                <div className="text-sm text-orange-600">#18</div>
              </div>
            </div>
          </div>
          <button className="btn btn-primary w-full mt-5 text-white">
            Ver Leaderboard
          </button>
        </div>
        <div className="w-full h-fit mt-4">
          <div className="text-2xl text-white font-semibold mb-3">
            Informações da Conta
          </div>
          <div className="w-full h-fit flex items-center flex-row justify-between my-3">
            <div className="w-fit h-full">
              <div className="text-xs text-white m-0">Email</div>
              <div className="text-lg text-orange-600 opacity-40 m-0 font-semibold">
                loremipsum@ua.pt
              </div>
            </div>
            <div className="w-fit underline text-sm text-primary">Editar</div>
          </div>
          <div className="w-full h-fit flex items-center flex-row justify-between my-3">
            <div className="w-fit h-full">
              <div className="text-xs text-white m-0">NMec</div>
              <div className="text-lg text-orange-600 opacity-40 m-0 font-semibold">
                123456
              </div>
            </div>
            <div className="w-fit underline text-sm text-primary">Editar</div>
          </div>
          <button className="btn btn-primary w-full mt-5 text-white">
            Reset Password
          </button>
        </div>
      </div>
    </BaseLayout>
  );
}
