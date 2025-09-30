export default function Loading() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <div
          key={i}
          className="animate-pulse p-4 rounded-lg shadow-sm space-y-2"
        >
          {/* Title placeholder */}
          <div className="h-5 bg-gray-300 rounded w-2/3" />
          {/* Content placeholder */}
          <div className="h-4 bg-gray-200 rounded w-full" />
          <div className="h-3 bg-gray-200 rounded w-5/6" />
          {/* Date placeholder */}
          <div className="h-3 bg-gray-200 rounded w-1/4 mt-2" />
        </div>
      ))}
    </div>
  );
}
