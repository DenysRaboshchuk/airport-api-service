import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center py-20 text-center px-4">
            <h1 className="text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
                Find Your Next Flight ✈️
            </h1>
            <p className="text-xl text-slate-600 max-w-2xl mb-8">
                A seamless and modern service for booking flight tickets to any destination worldwide.
            </p>
            <div className="flex gap-4">
                <Button asChild size="lg">
                    <Link to="/flights">Search Flights</Link>
                </Button>
                <Button asChild variant="outline" size="lg">
                    <Link to="/login">My Account</Link>
                </Button>
            </div>
        </div>
    )
}