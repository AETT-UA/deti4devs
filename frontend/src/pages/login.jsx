import { useForm } from "react-hook-form";
import { login } from "../api/auth";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const signIn = useSignIn();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const response = await login(data.username, data.password);
    if (response.status === 200) {
      if (
        signIn({
          auth: {
            token: response.data.access_token,
            type: response.data.token_type
          },
          userState: response.data.user,
        })
      ) {
        return navigate("/");
      } else {
        console.log("Failed to login");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-xs sm:max-w-lg px-2 mx-auto mt-8 p-6 bg-transparent">
      <div className="mb-4 flex justify-center cursor-pointer" onClick={() => navigate('/')}>
        <img src="/logo.png" alt="Logo" />
      </div>
      <h2 className="text-2xl font-medium tracking-wider mb-6 text-center text-primary-color">- Login -</h2>
      
      <div className="mb-4 relative">
        <input
          placeholder="Username"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.username ? 'border-red-500' : 'border-gray-300'}`}
          {...register("username", { required: "Username is required" })}
        />
        {errors.username && <span className="text-red-500 text-sm">{errors.username.message}</span>}
      </div>
      
      <div className="mb-4 relative">
        <input
          placeholder="Password"
          type="password"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
          {...register("password", { required: "Password is required" })}
        />
        {errors.password && <span className="text-red-500 text-sm">{errors.password.message}</span>}
      </div>
      
      <div className="text-center">
        <button type="submit" className="btn btn-primary w-full bg-secondary-color border-none">Login</button>
      </div>

      <div className="text-center mt-4">
        <span className="text-primary-color">Don't have an account? </span>
        <button type="button" className="text-secondary-color underline" onClick={() => navigate('/register')}>Register</button>
      </div>
      
      <div className="text-center mt-4">
        <button type="button" className="text-secondary-color underline" onClick={() => navigate('/recover')}>Forgot Password?</button>
      </div>
    </form>
  );
};
