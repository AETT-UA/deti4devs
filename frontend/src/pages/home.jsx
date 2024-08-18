import BaseLayout from "../components/BaseLayout";
export const Home = () => {
  return (
    <BaseLayout>
      <div className="h-fit w-full px-4">
        <div className="w-full rounded-xl bg-gradient-to-tr from-secondary to-[#444444] h-[45vh] flex flex-col items-center justify-center px-12">
          <div className="max-w-full object-contain mb-6">
            <img
              className="object-contain max-w-full max-h-full"
              src="public/loop.png"
            />
          </div>
          <div className="font-bold text-4xl bg-gradient-to-tr from-primary to-[#8B4615] text-transparent bg-clip-text drop-shadow-md">
            DETI4Devs
          </div>
          <div className="text-md text-center">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod
          </div>
          <div className="text-md text-center mt-1 underline">Saber mais</div>
        </div>
        <div className="w-full h-36 flex flex-row gap-4 my-3">
          <div className="w-full rounded-xl bg-secondary p-4 flex flex-col justify-between">
            <div className="text-xs text-left">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod
            </div>
            <div className="flex flex-row justify-between items-center h-8">
              <div className="text-xl font-semibold">Eventos</div>
              <img src="public/icons/circle_right.svg" className="w-8 h-8" />
            </div>
          </div>
          <div className="w-full rounded-xl bg-[#182361] p-4 flex flex-col justify-between">
            <div className="text-xs text-left">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod
            </div>
            <div className="flex flex-row justify-between items-center">
              <div className="text-xl font-semibold">Empresas</div>
              <img src="public/icons/circle_right.svg" className="w-8 h-8" />
            </div>
          </div>
        </div>
        <div className="w-full rounded-xl bg-primary h-36 flex flex-row justify-between items-center px-6">
          <div className="text-3xl font-semibold">Horário</div>
          <img
            src="public/icons/circle_right_30.svg"
            className="w-12 h-12 rotate-[-45deg]"
          />
        </div>
      </div>
    </BaseLayout>
  );
};
