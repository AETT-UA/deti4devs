import { useForm } from "react-hook-form";
import { login } from "../api/auth";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export const Login = () => {
  const {
    register,
    handleSubmit,
    watch,
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
            type: response.data.token_type,
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
    <>
      <Navbar />
      <form onSubmit={handleSubmit(onSubmit)} className="form-control">
        <input
          placeholder="Username"
          className="input input-bordered"
          {...register("username", { required: true })}
        />
        <input
          placeholder="Password"
          type="password"
          className="input input-bordered"
          {...register("password", { required: true })}
        />
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
    </>
  );
};
