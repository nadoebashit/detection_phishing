import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Shield } from 'lucide-react';
import { motion } from 'framer-motion';

const urlSchema = z.object({
  url: z.string().url({ message: "Please enter a valid URL (e.g., https://example.com)" }),
});

type URLFormValues = z.infer<typeof urlSchema>;

interface URLFormProps {
  onSubmit: (url: string) => void;
  isLoading: boolean;
}

export default function URLForm({ onSubmit, isLoading }: URLFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<URLFormValues>({
    resolver: zodResolver(urlSchema),
  });

  const onFormSubmit = (data: URLFormValues) => {
    onSubmit(data.url);
  };

  return (
    <motion.form 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit(onFormSubmit)} 
      className="w-full max-w-3xl mx-auto flex flex-col gap-2"
    >
      <div className="relative flex items-center w-full shadow-2xl rounded-2xl bg-[#0D1627] p-2 pr-2 border border-white/5 focus-within:border-[#00D4FF]/50 transition-colors">
        <div className="pl-4 pr-2 text-gray-500 hidden sm:block">HTTPS://</div>
        <input
          {...register('url')}
          type="text"
          placeholder="example.com/login"
          disabled={isLoading}
          className="flex-1 bg-transparent border-none outline-none text-white px-2 py-4 sm:py-2 text-lg placeholder:text-gray-600 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-primary text-black disabled:opacity-50 font-semibold h-12 px-6 rounded-xl sm:rounded-lg flex items-center justify-center gap-2 hover:bg-[#00D4FF]/90 transition-colors"
        >
          {isLoading ? (
            <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
              <Shield className="w-5 h-5" />
            </motion.div>
          ) : (
            <Shield className="w-5 h-5" />
          )}
          <span className="hidden sm:inline">{isLoading ? 'Scanning...' : 'Check URL'}</span>
        </button>
      </div>
      {errors.url && (
        <motion.span 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-[#FF4444] text-sm mt-2 ml-4 font-medium"
        >
          {errors.url.message}
        </motion.span>
      )}
    </motion.form>
  );
}
