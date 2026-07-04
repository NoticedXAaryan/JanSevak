export type UserRole = 
  | "super_admin" 
  | "org_admin" 
  | "org_viewer" 
  | "mp" 
  | "collector" 
  | "citizen";

export interface UserSession {
  id: string;
  email?: string;
  phone?: string;
  name: string;
  role: UserRole;
  orgId?: string;
  orgType?: string;
}

// In a real app, this would read from a JWT stored in an HttpOnly cookie
// For the frontend demo, we'll use a simple mock store or localStorage if needed.

export function getSession(): UserSession | null {
  if (typeof window === "undefined") return null;
  
  try {
    const session = localStorage.getItem("jansevak_session");
    if (session) {
      return JSON.parse(session);
    }
  } catch (e) {
    console.error("Failed to parse session", e);
  }
  return null;
}

export function setSession(session: UserSession) {
  if (typeof window !== "undefined") {
    localStorage.setItem("jansevak_session", JSON.stringify(session));
  }
}

export function clearSession() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("jansevak_session");
  }
}

export function isAuthenticated(): boolean {
  return getSession() !== null;
}

export function hasRole(requiredRoles: UserRole[]): boolean {
  const session = getSession();
  if (!session) return false;
  return requiredRoles.includes(session.role);
}
