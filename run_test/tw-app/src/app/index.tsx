import { Image, Link, Text, View } from "@/components/tw";

const categories = ["Dairy", "Fruits", "Snacks", "Drinks", "Bakery", "Care"];

export default function Home() {
  return (
    <View className="flex-1 bg-brand-light px-5 pt-16">
      <View className="rounded-2xl bg-brand-yellow p-5">
        <Text className="text-sm font-semibold text-neutral-700">
          Delivery in
        </Text>
        <Text className="text-4xl font-extrabold text-neutral-900">
          10 minutes
        </Text>
        <Text className="mt-1 text-neutral-700">Deliver to Home · Bengaluru</Text>
      </View>

      <Text className="mb-3 mt-6 text-lg font-bold text-neutral-900">
        Shop by category
      </Text>
      <View className="flex-row flex-wrap gap-3">
        {categories.map((c) => (
          <View
            key={c}
            className="w-[30%] items-center rounded-xl bg-white p-3 shadow-sm"
          >
            <Image
              className="h-12 w-12 rounded-full bg-brand-light"
              source={require("../../assets/icon.png")}
              contentFit="cover"
            />
            <Text className="mt-2 text-xs font-medium text-neutral-800">{c}</Text>
          </View>
        ))}
      </View>

      <Link
        href="/"
        className="mt-8 rounded-xl bg-brand py-4 text-center text-base font-bold text-white"
      >
        Start shopping
      </Link>
    </View>
  );
}
