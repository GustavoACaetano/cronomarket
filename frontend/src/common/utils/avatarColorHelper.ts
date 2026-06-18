export function getAvatarColor(username: string): string {
    if (!username) return '#10b981'; // Fallback to emerald primary
    
    // Hash function to get a deterministic index based on username
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    // Curated premium color palette (soft pastel and pleasant colors)
    const colors = [
        '#10b981', // Emerald
        '#3b82f6', // Blue
        '#8b5cf6', // Violet
        '#ec4899', // Pink
        '#f59e0b', // Amber
        '#06b6d4', // Cyan
        '#f43f5e', // Rose
        '#6366f1', // Indigo
        '#14b8a6', // Teal
        '#84cc16', // Lime
    ];
    
    const index = Math.abs(hash) % colors.length;
    return colors[index] ?? '#10b981';
}
