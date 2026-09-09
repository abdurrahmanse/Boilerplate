import { auth } from "@repo/auth/server";
import { notFound, redirect } from "next/navigation";
import { Header } from "../components/header";

interface SearchPageProperties {
  searchParams: Promise<{
    q: string;
  }>;
}

export const generateMetadata = async ({
  searchParams,
}: SearchPageProperties) => {
  const { q } = await searchParams;

  return {
    title: `${q} - Search results`,
    description: `Search results for ${q}`,
  };
};

const SearchPage = async ({ searchParams }: SearchPageProperties) => {
  const { q } = await searchParams;
  
  if (!q) {
    redirect("/");
  }

  let pages: any[] = [];
  try {
    const res = await fetch(`http://localhost:8000/pages?q=${encodeURIComponent(q)}`, { cache: "no-store" });
    if (res.ok) {
      pages = await res.json();
    }
  } catch (error) {
    console.error("Failed to fetch pages", error);
  }

  const { orgId } = await auth();

  if (!orgId) {
    notFound();
  }

  return (
    <>
      <Header page="Search" pages={["Building Your Application"]} />
      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          {pages.map((page) => (
            <div className="aspect-video rounded-xl bg-muted/50" key={page.id}>
              {page.name}
            </div>
          ))}
        </div>
        <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
      </div>
    </>
  );
};

export default SearchPage;
