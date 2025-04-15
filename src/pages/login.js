import React, { useState } from "react";
import { useRouter } from "next/router";
import { johnWeeklyData, sarahWeeklyData } from "./placeholderData";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// This is a simple login form component using React and Next.js
function Login({ setUserData }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  // Handle login form submission
  const handleLogin = async (formData) => {
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      localStorage.setItem("token", data.token); // Save the token in localStorage
      localStorage.setItem("user_id", data.user_id); // Save the user ID if needed
      router.push("/profile"); // Redirect to the profile page
    } catch (err) {
      console.error(err.message);
    }
  };

  const updateUserData = async (updatedData) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/logs/<user_id>", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updatedData),
      });
      if (!response.ok) {
        throw new Error("Failed to update user data");
      }
      const data = await response.json();
      console.log("User data updated:", data);
    } catch (err) {
      console.error(err.message);
    }
  };

  // Render the login form
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md dark:bg-gray-800 p-6 space-y-4">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white text-center">
          Login to Your Account
        </h2>
        <form className="space-y-4" onSubmit={(e) => {
          e.preventDefault();
          handleLogin({ email, password });
        }}>
          {/* Email Input */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-4 py-2 border rounded-lg text-gray-900 bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-primary-500 focus:border-primary-500"
              placeholder="your@email.com"
              required
            />
          </div>
          {/* Password Input */}
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-4 py-2 border rounded-lg text-gray-900 bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-primary-500 focus:border-primary-500"
              placeholder="••••••••"
              required
            />
          </div>
          {/* Error Message */}
          {error && (
            <p className="text-sm text-red-500 dark:text-red-400 text-center">{error}</p>
          )}
          {/* Submit Button */}
          <button
            type="submit"
            className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-800"
          >
            Login
          </button>
        </form>
        {/* Register Link */}
        <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
          Don't have an account?{" "}
          <a
            href="/register"
            className="text-blue-600 hover:underline dark:text-blue-500"
          >
            Register
          </a>
        </p>
      </div>
    </div>
  );
}

export default Login;