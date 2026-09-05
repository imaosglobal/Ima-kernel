import { useState, useEffect, useCallback } from "react";

const STORAGE_KEY = "ima-user";

const defaultUser = {
  name: "",
  lang: "he",
  onboarded: false,
  goals: [],
  preferences: { tone: "warm", responseLength: "medium" },
  conversations: [],
  memory: [],
};

export function useUser() {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? { ...defaultUser, ...JSON.parse(stored) } : defaultUser;
    } catch {
      return defaultUser;
    }
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
  }, [user]);

  const updateUser = useCallback((updates) => {
    setUser((prev) => ({ ...prev, ...updates }));
  }, []);

  const completeOnboarding = useCallback((data) => {
    setUser((prev) => ({ ...prev, ...data, onboarded: true }));
  }, []);

  const addConversation = useCallback((entry) => {
    setUser((prev) => ({
      ...prev,
      conversations: [...prev.conversations, entry],
    }));
  }, []);

  const clearConversations = useCallback(() => {
    setUser((prev) => ({ ...prev, conversations: [] }));
  }, []);

  const addMemory = useCallback((item) => {
    setUser((prev) => ({
      ...prev,
      memory: [...prev.memory, { id: Date.now(), ...item }],
    }));
  }, []);

  const removeMemory = useCallback((id) => {
    setUser((prev) => ({
      ...prev,
      memory: prev.memory.filter((m) => m.id !== id),
    }));
  }, []);

  const clearMemory = useCallback(() => {
    setUser((prev) => ({ ...prev, memory: [] }));
  }, []);

  const resetUser = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setUser(defaultUser);
  }, []);

  return {
    user,
    updateUser,
    completeOnboarding,
    addConversation,
    clearConversations,
    addMemory,
    removeMemory,
    clearMemory,
    resetUser,
  };
}
