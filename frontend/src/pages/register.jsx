import { useForm } from "react-hook-form";
import { signUp } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { AiOutlineCheck } from 'react-icons/ai';

export const Register = () => {
  const navigate = useNavigate();
  const [isTouched, setIsTouched] = useState({
    username: false,
    email: false,
    full_name: false,
    nmec: false,
    password: false,
    verify_password: false,
  });

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, touchedFields },
    trigger,
  } = useForm();

  const onSubmit = async (data) => {
    const response = await signUp(data);

    if (response.status === 200) {
      navigate("/login");
    }
  };

  const handleBlur = (field) => {
    setIsTouched((prevState) => ({
      ...prevState,
      [field]: true,
    }));
    trigger(field); // Trigger validation on blur
  };

  useEffect(() => {
    Object.keys(touchedFields).forEach((field) => {
      if (touchedFields[field]) {
        trigger(field);
      }
    });
  }, [touchedFields, trigger]);

  const renderIcon = (field, error) => {
    const value = watch(field);
    if (value && isTouched[field] && !error) {
      return <AiOutlineCheck className="absolute right-2 top-1/2 transform -translate-y-1/2 text-white font-bold" />;
    }
    return null;
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-xs sm:max-w-lg px-2 mx-auto mt-8 p-6 bg-transparent">
      <div className="mb-4 flex justify-center cursor-pointer" onClick={() => navigate('/')}>
        <img src="/logo.png" alt="Logo" />
      </div>
      <h2 className="text-2xl font-medium tracking-wider mb-6 text-center text-primary-color">- Register -</h2>
      
      <div className="mb-4 relative">
        <input
          type="text"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.username ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Username"
          {...register("username", {
            required: "Username is required",
            maxLength: { value: 20, message: "Username cannot exceed 20 characters" },
            minLength: { value: 5, message: "Username must be at least 5 characters" },
          })}
          onBlur={() => handleBlur('username')}
        />
        {renderIcon('username', errors.username)}
        {errors.username && <span className="text-red-500 text-sm">{errors.username.message}</span>}
      </div>
      
      <div className="mb-4 relative">
        <input
          type="email"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Email"
          {...register("email", {
            required: "Email is required",
            pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Invalid email address" },
          })}
          onBlur={() => handleBlur('email')}
        />
        {renderIcon('email', errors.email)}
        {errors.email && <span className="text-red-500 text-sm">{errors.email.message}</span>}
      </div>
      
      <div className="mb-4 relative">
        <input
          type="text"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.full_name ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Full Name"
          {...register("full_name", { required: "Full name is required" })}
          onBlur={() => handleBlur('full_name')}
        />
        {renderIcon('full_name', errors.full_name)}
        {errors.full_name && <span className="text-red-500 text-sm">{errors.full_name.message}</span>}
      </div>
      
      <div className="mb-4 relative">
        <input
          type="text"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.nmec ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="NMEC"
          {...register("nmec", {
            required: "NMEC is required",
            pattern: { value: /^\d{1,6}$/, message: "NMEC must be a number with up to 6 digits" },
          })}
          onBlur={() => handleBlur('nmec')}
        />
        {renderIcon('nmec', errors.nmec)}
        {errors.nmec && <span className="text-red-500 text-sm">{errors.nmec.message}</span>}
      </div>
      
      <div className="mb-4 relative">
        <input
          type="password"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Password"
          {...register("password", {
            required: "Password is required",
            minLength: { value: 6, message: "Password must be at least 6 characters long" },
          })}
          onBlur={() => handleBlur('password')}
        />
        {renderIcon('password', errors.password)}
        {errors.password && <span className="text-red-500 text-sm">{errors.password.message}</span>}
      </div>
      
      <div className="mb-6 relative">
        <input
          type="password"
          className={`input input-bordered bg-primary-color w-full text-white ${errors.verify_password ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Verify Password"
          {...register("verify_password", {
            required: "Please verify your password",
            validate: value => value === watch('password') || "Passwords do not match",
          })}
          onBlur={() => handleBlur('verify_password')}
        />
        {renderIcon('verify_password', errors.verify_password)}
        {errors.verify_password && <span className="text-red-500 text-sm">{errors.verify_password.message}</span>}
      </div>
      
      <div className="text-center">
        <input type="submit" className="btn btn-primary w-full bg-secondary-color border-none" value="Register" />
      </div>
    </form>
  );
};
