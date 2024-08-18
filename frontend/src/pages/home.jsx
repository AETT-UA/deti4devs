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
        </div>
        <div className="w-full h-36 flex flex-row gap-4 my-3">
          <div className="w-full rounded-xl bg-secondary"></div>
          <div className="w-full rounded-xl bg-secondary"></div>
        </div>
        <div className="w-full rounded-xl bg-secondary h-36"></div>
      </div>
    </BaseLayout>
  );
};
