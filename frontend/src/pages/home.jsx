import useAuthUser from "react-auth-kit/hooks/useAuthUser";
import useSignOut from "react-auth-kit/hooks/useSignOut";
import { useNavigate } from "react-router-dom";
export const Home = () => {
  const auth = useAuthUser();
  const signOut = useSignOut();
  const navigate = useNavigate();

  const logout = () => {
    signOut();
    navigate("/login");
  }

  return (
    <>
      <p className="text-xl">Hello {auth.username}</p>
      <button onClick={logout} className="btn btn-primary">
        Logout
      </button>
    </>
  );
};
