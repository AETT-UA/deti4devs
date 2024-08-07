import { useForm } from "react-hook-form";
import { signUp } from "../api/auth";
import { useNavigate } from "react-router-dom";

export const Register = () => {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = async (data) => {
    const response = await signUp(data);

    if (response.status === 200) {
      navigate("/login");
    }
  }


  return (
    <form onSubmit={handleSubmit(onSubmit)} className="form-control">
      <input
        type="text"
        className="input input-bordered"
        placeholder="username"
        {...register("username", { required: true, max: 20, min: 5 })}
      />
      <input
        type="email"
        className="input input-bordered"
        placeholder="email"
        {...register("email", { required: true })}
      />
      <input
        type="text"
        className="input input-bordered"
        placeholder="full_name"
        {...register("full_name", { required: true })}
      />
      <input
        type="password"
        className="input input-bordered"
        placeholder="password"
        {...register("password", { required: true })}
      />

      <input type="submit" className="btn btn-primary"/>
    </form>
  );
};
