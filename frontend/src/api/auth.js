import { api } from "./api";

export const login = async (username, password) => {
  const response = await api.post(
    "/auth/token",
    { username, password },
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  if (response.status !== 200) {
    throw new Error("Failed to login");
  }

  const userData = await api.get("/auth/me", {
    headers: {
      Authorization: `${response.data.token_type} ${response.data.access_token}`,
    },
  });

  if (userData.status !== 200) {
    throw new Error("Failed to get user data");
  }

  response.data.user = userData.data;
  return response;
};

export const signUp = async (user) => {
  const response = await api.post("/auth/register", user);

  if (response.status !== 200) {
    throw new Error("Failed to register");
  }

  return response;
};
