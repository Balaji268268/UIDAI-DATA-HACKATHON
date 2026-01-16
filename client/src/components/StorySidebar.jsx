import React from 'react';
import { Baby, Users, ShieldAlert, GraduationCap, LayoutDashboard } from 'lucide-react';

const StorySidebar = ({ currentView, onViewChange }) => {
    const menuItems = [
        { id: 'dashboard', label: 'Main Dashboard', icon: LayoutDashboard, color: 'text-gray-400' },
        { id: 'integrity', label: 'Integrity Shield', icon: ShieldAlert, color: 'text-red-500' },
        { id: 'ghost', label: 'Ghost Child Finder', icon: Baby, color: 'text-purple-400' },
        { id: 'migration', label: 'Migration Radar', icon: Users, color: 'text-blue-400' },
        { id: 'youth', label: 'Youth Awareness', icon: GraduationCap, color: 'text-yellow-400' },
    ];

    return (
        <div className="w-64 bg-black/60 backdrop-blur-xl border-r border-white/10 flex flex-col h-screen fixed left-0 top-0 z-50">
            <div className="p-6 border-b border-white/10">
                <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    Aadhaar 360
                </h2>
                <p className="text-xs text-gray-500 mt-1 uppercase tracking-widest">Innovation Suite</p>
            </div>

            <div className="flex-1 py-4 space-y-2">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = currentView === item.id;

                    return (
                        <button
                            key={item.id}
                            onClick={() => onViewChange(item.id)}
                            className={`w-full px-6 py-3 flex items-center gap-3 transition-all duration-300 border-l-2
                ${isActive
                                    ? 'border-cyan-500 bg-white/5 text-white'
                                    : 'border-transparent text-gray-400 hover:bg-white/5 hover:text-white'
                                }`}
                        >
                            <Icon size={18} className={isActive ? item.color : 'text-gray-500'} />
                            <span className="text-sm font-medium">{item.label}</span>
                        </button>
                    );
                })}
            </div>

            <div className="p-6 border-t border-white/10">
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                    <p className="text-xs text-green-400 font-mono flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        System Online
                    </p>
                </div>
            </div>
        </div>
    );
};

export default StorySidebar;
