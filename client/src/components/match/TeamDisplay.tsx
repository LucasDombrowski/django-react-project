import React from 'react';
import { Team } from '@/libs/types/models/team'; // Updated path alias
import clsx from 'clsx'; // Import clsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"; // Import Avatar components
import { cn } from '@/libs/utils'; // Import cn for potential class merging on Avatar
import matchDetailStrings from '@/libs/keychains/matchDetail.json'; // Import keychain

interface TeamDisplayProps {
    team: Team;
    // nameColorClass?: string; // Removed this prop
}

const TeamDisplay: React.FC<TeamDisplayProps> = ({ team }) => {
    if (!team) {
        return null; // Or some placeholder if a team is expected but not provided
    }

    // const defaultNameColor = 'text-gray-800'; // Old default
    const h2Classes = clsx('text-2xl font-semibold mt-2', 'text-foreground'); // Standardized to text-foreground

    return (
        <div className="flex flex-col items-center w-1/3">
            <Avatar className={cn("w-32 h-32 mb-3 shadow-md")}> {/* Increased size & added shadow */}
                <AvatarImage src={team.logo_url || undefined} alt={`${team.name}${matchDetailStrings.alt_logo_suffix}`} className="object-cover" />
                <AvatarFallback className="text-3xl">
                    {team.name.substring(0, 2).toUpperCase()} {/* Example Fallback: First two letters */}
                </AvatarFallback>
            </Avatar>
            <h2 className={h2Classes}>
                {team.name}
            </h2>
        </div>
    );
};

export default TeamDisplay; 