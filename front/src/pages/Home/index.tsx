import { Button } from "@/components/ui/button";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";

function Home() {
  const navigate = useNavigate();

  const formSchema = z.object({
    songName: z
      .string({
        required_error: "Por favor digite antes de prosseguir.",
      })
      .nonempty("Nome da música é obrigatório"),
    artistName: z
      .string({
        required_error: "Por favor digite antes de prosseguir.",
      })
      .nonempty("Nome do artista é obrigatório"),
  });
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });
  return (
    <div className="relative home flex flex-col justify-center items-center w-screen min-h-screen bg-[var(--color-primary)] text-white px-8 gap-8 !overflow-hidden">
      <div className="w-40 h-72 md:w-[297px] md:h-[447px] absolute top-[-2rem] md:top-0 left-[-1rem] bg-contain bg-center bg-no-repeat bg-[url('/design-lt.svg')]"></div>{" "}
      <div className="w-64 h-72 md:w-[432px] md:h-[466px] absolute top-[-2rem]  right-0 bg-contain bg-center bg-no-repeat bg-[url('/design-rt.svg')] overflow-hidden"></div>{" "}
      <div className="w-52 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-5rem]  right-0 bg-contain bg-center bg-no-repeat bg-[url('/design-rb.svg')] !overflow-clip bg-center overflow-x-hidden overflow-y-hidden"></div>{" "}
      <div className="w-52 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-5rem]  left-0 bg-contain bg-center bg-no-repeat bg-[url('/design-lb.svg')] !overflow-clip bg-center overflow-x-hidden overflow-y-hidden"></div>{" "}
      <div className="flex flex-col gap-4 items-center max-w-sm z-10">
        <img src="/logo.svg" alt="Logo" className="w-52 " />
        <h4 className="text-lg text-[#979797]">
          Música sempre foi som. No futuro, será imagem também.
        </h4>
      </div>
      <div className="flex max-w-2xl w-full items-center z-10">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit((data) => {
              console.log(data);
              navigate("/song-list");
            })}
            className="w-full flex flex-col gap-4 items-center"
          >
            <FormField
              {...form.register("songName")}
              render={({ field }) => (
                <FormItem className="w-full">
                  <FormLabel className="text-md">Nome da música</FormLabel>
                  <Input
                    {...field}
                    type="text"
                    placeholder="Digite o nome da música..."
                    className="rounded-lg w-full"
                  />
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              {...form.register("artistName")}
              render={({ field }) => (
                <FormItem className="w-full">
                  <FormLabel className="text-md">Nome do artista</FormLabel>
                  <Input
                    {...field}
                    type="text"
                    placeholder="Digite o nome do artista original da música..."
                    className="rounded-lg w-full"
                  />
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button
              type="submit"
              className="w-full mt-4 max-w-3xs md:max-w-xs items-self-center !bg-[#497289] hover:!bg-[#3e5c7d] hover:!border-white"
            >
              Enviar
            </Button>
          </form>
        </Form>
      </div>
      <p className="footer text-center justify-self-end">
        © 2024 ALL RIGHTS RESERVED
      </p>
    </div>
  );
}

export default Home;
