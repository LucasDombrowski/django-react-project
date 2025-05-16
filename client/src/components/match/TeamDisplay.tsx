import React from 'react';
import { Team } from '../../libs/types/models/team'; // Assuming your Team interface is here
import clsx from 'clsx'; // Import clsx

interface TeamDisplayProps {
    team: Team;
    nameColorClass?: string;
}

const TeamDisplay: React.FC<TeamDisplayProps> = ({ team, nameColorClass }) => {
    if (!team) {
        return null; // Or some placeholder if a team is expected but not provided
    }

    const defaultNameColor = 'text-gray-800'; // Default color if none provided
    const h2Classes = clsx('text-2xl font-semibold', nameColorClass || defaultNameColor);

    return (
        <div className="flex flex-col items-center w-1/3">
            {team.logo_url && (
                <div className="flex items-center justify-center w-32 h-32 mb-3 rounded-lg object-contain shadow-md p-4">
                    <img
                        src={team.logo_url}
                        alt={`${team.name} logo`}
                        className="w-full h-full object-contain"
                    />
                </div>
            )}
            <h2 className={h2Classes}>
                {team.name}
            </h2>
        </div>
    );
};

export default TeamDisplay; 