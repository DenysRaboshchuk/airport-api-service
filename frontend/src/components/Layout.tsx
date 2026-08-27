import {Link, Outlet} from "react-router-dom"
import {Button} from "@/components/ui/button"

export default function Layout() {
    return (
        <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
            {/* Navigation Bar */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2 font-bold text-xl text-slate-900 hover:opacity-90">
                        <span className="text-2xl">✈️</span>
                        <span>Airport Service</span>
                    </Link>

                    {/* Navigation Links */}
                    <nav className="flex items-center gap-6">
                        <Link to="/flights"
                              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                            Flights
                        </Link>
                        <Link to="/orders"
                              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                            My Tickets
                        </Link>
                    </nav>


                    {/* Auth Buttons */}
                    <div className="flex items-center gap-3">
                        <Button asChild variant="ghost" size="sm">
                            <Link to="/login">Sign In</Link>
                        </Button>
                        <Button asChild size="sm">
                            <Link to="/register">Sign Up</Link>
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content Area */}
            <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <Outlet />
            </main>

            {/* Footer */}
            <footer
                className="bg-white border-t border-slate-200 py-6 text-center text-sm text-slate-500">
                &copy; {new Date().getFullYear()} Airport API Service. All rights reserved.
            </footer>
        </div>
    )
}