import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const Recovery = () => {
  const navigate = useNavigate();
  const [submitted, setSubmitted] = useState(false);
  const [countdown, setCountdown] = useState(3);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    // Simulate the recovery process
    setSubmitted(true);
  };

  useEffect(() => {
    if (submitted) {
      const timer = setInterval(() => {
        setCountdown((prevCountdown) => {
          if (prevCountdown === 1) {
            clearInterval(timer);
            navigate('/');
          }
          return prevCountdown - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [submitted, navigate]);

  return (
    <div className="w-full max-w-xs sm:max-w-lg px-2 mx-auto mt-8 p-6 bg-transparent">
      <div className="mb-4 flex justify-center cursor-pointer" onClick={() => navigate('/')}>
        <img src="/logo.png" alt="Logo" />
      </div>
      <h2 className="text-2xl font-medium tracking-wider mb-6 text-center text-primary-color">- Recover Password -</h2>
      
      {!submitted ? (
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-4 relative">
            <input
              type="email"
              className={`input input-bordered bg-primary-color w-full text-white ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
              placeholder="Email"
              {...register("email", {
                required: "Email is required",
                pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Invalid email address" },
              })}
            />
            {errors.email && <span className="text-red-500 text-sm">{errors.email.message}</span>}
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
            />
            {errors.nmec && <span className="text-red-500 text-sm">{errors.nmec.message}</span>}
          </div>
          
          <div className="text-center">
            <button type="submit" className="btn btn-primary w-full bg-secondary-color border-none">Recover</button>
          </div>
        </form>
      ) : (
        <div className="text-center">
          <p className="text-primary-color">Sent to the email if the inserted data is correct</p>
          <p className="text-primary-color">Redirecting in {countdown}...</p>
        </div>
      )}
    </div>
  );
};
